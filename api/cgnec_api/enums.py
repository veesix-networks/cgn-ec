from enum import Enum


class NATEventEnum(str, Enum):
    ADDRESS_MAPPING = "address-mapping"
    PORT_MAPPING = "port-mapping"
    PORT_BLOCK_MAPPING = "port-block-mapping"
    SESSION_MAPPING = "session-mapping"


class NATEventTypeEnum(int, Enum):
    CREATED = 1
    DELETED = 2
    UPDATED = 3
