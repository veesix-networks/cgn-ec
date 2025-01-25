from influxdb import InfluxDBClient
from structlog import get_logger

from consumer.outputs.base import BaseOutput

logger = get_logger("cgn-ec.outputs.influxv1")


class InfluxV1Output(BaseOutput):
    def __init__(
        self,
        address: str,
        port: int,
        database: str = "cgnat",
        username: str = "",
        password: str = "",
    ):
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self._client = None

    def process_event(self, metrics: list[dict]) -> bool:
        logger.debug("Processing event data")
        if not self._client:
            self._client = InfluxDBClient(
                self.address, self.port, self.username, self.password, self.database
            )

        success = self._client.write_points([metric.model_dump() for metric in metrics])
        return success
