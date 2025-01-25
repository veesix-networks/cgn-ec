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


class NATProtocolEnum(str, Enum):
    ICMP = 1
    TCP = 6
    UDP = 17

    @classmethod
    def from_string(cls, name: str):
        try:
            return cls[name.upper()].value
        except KeyError:
            raise ValueError(f"Invalid protocol name: {name}")
