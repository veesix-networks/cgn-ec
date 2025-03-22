from confluent_kafka import Producer
import json
import socket
import radiusd
import os

conf = {
    "bootstrap.servers": os.environ["KAFKA_BOOTSTRAP_SERVER"],
    "client.id": socket.gethostname(),
}

producer = Producer(conf)


def transform_tuple(data):
    transformed_dict = {}

    for t in data:
        k, v = t
        transformed_dict[k] = v

    return transformed_dict


def instantiate(p):
    print("*** instantiate ***")
    print(p)


"""
def preacct(p):
    print("*** preacct ***")
    print(p)
    return freeradius.RLM_MODULE_OK
"""


def accounting(p):
    print("*** accounting ***")
    accounting_attributes = transform_tuple(p)
    producer.produce(
        "cgnat.radius.accounting",
        value=json.dumps(accounting_attributes).encode("UTF-8"),
    )
    radiusd.radlog(radiusd.L_DBG, str(accounting_attributes))
    return radiusd.RLM_MODULE_OK
