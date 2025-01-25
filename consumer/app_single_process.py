import json

from time import time
from os import getpid
from confluent_kafka import Consumer, Message
from time import sleep
from multiprocessing import Value, Lock
from threading import Thread
from structlog import get_logger

from consumer.handlers.generic import BaseHandler
from consumer.config import settings
from consumer.logger import setup_logging

logger = get_logger()

metrics_count = Value("i", 0)
metrics_lock = Lock()


def _process_metrics(
    records: list[Message],
    consumer: Consumer,
    handler: BaseHandler,
    metrics_count: Value,
    metrics_lock: Lock,
):
    metrics = []
    for msg in records:
        message = json.loads(msg.value().decode("utf-8"))
        metric = handler.parse_message(message)
        if not metric:
            continue

        metrics.append(metric)

    handler.process_outputs(metrics)

    metrics_total = len(metrics)
    with metrics_lock:
        metrics_count.value += metrics_total

    metrics.clear()
    logger.debug(f"Total metrics processed by process[{getpid()}]: {metrics_total}")
    consumer.commit()


def build_config():
    config = {
        "group.id": settings.KAFKA_GROUP_ID,
        "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
        "fetch.max.bytes": 524288000,
        "partition.assignment.strategy": "roundrobin",
    }
    return config


def print_metrics_count(metrics_count: Value):
    prev_count = 0
    prev_time = time()  # Record the initial time

    while True:
        current_count = metrics_count.value
        current_time = time()

        # Calculate metrics processed in the interval
        metrics_diff = current_count - prev_count
        time_diff = current_time - prev_time

        if time_diff > 0:
            avg_metrics_per_second = metrics_diff / time_diff
        else:
            avg_metrics_per_second = 0

        logger.info(
            "Metric statistics",
            total_metrics_processed=f"Total metrics processed: {current_count}",
            avg_metrics_per_second=f"Average metrics per second: {avg_metrics_per_second:.2f}",
        )

        # Update previous metrics and time for the next iteration
        prev_count = current_count
        prev_time = current_time

        sleep(5)


if __name__ == "__main__":
    setup_logging()

    # metric worker
    t = Thread(target=print_metrics_count, args=(metrics_count,), daemon=True)
    t.start()

    handler = settings.HANDLER(outputs=settings.OUTPUTS)
    config = build_config()
    consumer = Consumer(config)
    consumer.subscribe([handler.TOPIC])

    while True:
        try:
            records = consumer.consume(settings.KAFKA_MAX_RECORDS_POLL, timeout=1)
            if not records or records is None:
                sleep(0.01)
                continue

            _process_metrics(records, consumer, handler, metrics_count, metrics_lock)
        except Exception as err:
            logger.error(f"Terminating worker with pid: {getpid()} due to error: {err}")
            consumer.close()
            break

        sleep(0.01)

    consumer.close()
