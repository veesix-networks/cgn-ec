from requests import Session
from structlog import get_logger

from consumer.outputs.base import BaseOutput

logger = get_logger("cgn-ec.outputs.http")


class HTTPOutput(BaseOutput):
    def __init__(self, url: str, headers: dict = {}):
        self.url = url
        self.headers = headers
        self._session = Session(headers=self.headers)

    def process_event(self, data: dict):
        logger.debug("Processing event data")
        with self._session as session:
            session.post(self.url, json=data)
