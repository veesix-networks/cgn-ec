from typing import Any
from pydantic_settings import BaseSettings

from consumer import handlers
from consumer import outputs


class Settings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9094"
    KAFKA_GROUP_ID: str = "syslog-consumers"
    KAFKA_MAX_RECORDS_POLL: int = 500

    HANDLER: Any = handlers.NFWareSyslogHandler
    BATCH_SIZE: int = 30000
    OUTPUTS: list[Any] = [
        outputs.TimeScaleDBOutput(
            "tsdb", 5432, "cgnat", "password123", batch_size=BATCH_SIZE
        )
    ]


settings = Settings()
