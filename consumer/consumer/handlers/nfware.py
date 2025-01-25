# https://docs.nfware.com/en/6.3/nat/logging.html#message-format
# Address mapping (Static NAT / 1-1 NAT): A VRF 0 INT 10.0.0.1 EXT 100.64.0.1
# Port Mapping: A VRF 0 6 INT 10.0.0.1:57938 EXT 100.64.0.1:28475
# Session: A VRF 0 6 INT 10.0.0.1:57938 EXT 100.64.0.1:28475 DST 185.165.123.206:443 DIR OUT
# Port Blocks: A VRF 0 INT 10.0.0.1 EXT 100.64.0.1:1024-1535
# Typically deterministic CGN should be used with port ranges to avoid large logs

import regex as re
from typing import Any
from datetime import datetime
from structlog import get_logger

from consumer.handlers.generic import GenericSyslogHandler
from consumer.enums import NATEventTypeEnum, NATEventEnum


logger = get_logger("cgn-ec.handlers.nfware")


class NFWareSyslogHandler(GenericSyslogHandler):
    TOPIC = "cgnat.syslog.nfware"

    REGEX_ADDRESS_MAPPING = (
        r"([AD]) VRF (\d+) INT (\d+\.\d+\.\d+\.\d+) EXT (\d+\.\d+\.\d+\.\d+)$"
    )
    REGEX_PORT_MAPPING = r"([AD]) VRF (\d+) (\d+) INT (\d+\.\d+\.\d+\.\d+):(\d+) EXT (\d+\.\d+\.\d+\.\d+):(\d+)$"
    REGEX_SESSION_MAPPING = r"([AD]) VRF (\d+) (\d+) INT (\d+\.\d+\.\d+\.\d+):(\d+) EXT (\d+\.\d+\.\d+\.\d+):(\d+) DST (\d+\.\d+\.\d+\.\d+):(\d+) DIR (OUT|IN)$"
    REGEX_PORT_BLOCK_MAPPING = r"([AD]) VRF (\d+) INT (\d+\.\d+\.\d+\.\d+) EXT (\d+\.\d+\.\d+\.\d+):(\d+)-(\d+)$"

    PATTERNS = [
        (re.compile(REGEX_SESSION_MAPPING), "parse_session_mapping"),
        (re.compile(REGEX_PORT_MAPPING), "parse_port_mapping"),
        (re.compile(REGEX_PORT_BLOCK_MAPPING), "parse_port_block_mapping"),
        (re.compile(REGEX_ADDRESS_MAPPING), "parse_address_mapping"),
    ]

    def parse_address_mapping(
        self, data: tuple[str | Any], host_ip: str, timestamp: datetime
    ) -> dict:
        __event_type__ = NATEventEnum.ADDRESS_MAPPING
        if len(data) != 4:
            return

        logger.debug("Parsing Address Mapping", data=data)
        metric = {
            "type": __event_type__,
            "timestamp": timestamp,
            "host": host_ip,
            "event": self.event_to_enum(data[0]),
            "vrf_id": int(data[1]),
            "src_ip": data[2],
            "x_ip": data[3],
        }
        return metric

    def parse_port_mapping(
        self, data: tuple[str | Any], host_ip: str, timestamp: datetime
    ) -> dict:
        __event_type__ = NATEventEnum.PORT_MAPPING
        if len(data) != 7:
            return

        logger.debug("Parsing Port Mapping", data=data)
        metric = {
            "type": __event_type__,
            "timestamp": timestamp,
            "host": host_ip,
            "event": self.event_to_enum(data[0]),
            "vrf_id": int(data[1]),
            "protocol": int(data[2]),
            "src_ip": data[3],
            "src_port": int(data[4]),
            "x_ip": data[5],
            "x_port": int(data[6]),
        }
        return metric

    def parse_session_mapping(
        self, data: tuple[str | Any], host_ip: str, timestamp: datetime
    ) -> dict:
        __event_type__ = NATEventEnum.SESSION_MAPPING
        if len(data) != 10:
            return

        logger.debug("Parsing Session Mapping", data=data)
        metric = {
            "type": __event_type__,
            "timestamp": timestamp,
            "host": host_ip,
            "event": self.event_to_enum(data[0]),
            "vrf_id": int(data[1]),
            "protocol": int(data[2]),
            "src_ip": data[3],
            "src_port": data[4],
            "x_ip": data[5],
            "x_port": int(data[6]),
            "dst_ip": data[7],
            "dst_port": int(data[8]),
        }
        return metric

    def parse_port_block_mapping(
        self, data: tuple[str | Any], host_ip: str, timestamp: datetime
    ) -> dict:
        __event_type__ = NATEventEnum.PORT_BLOCK_MAPPING
        if len(data) != 6:
            return

        logger.debug("Parsing Port Block Mapping", data=data)
        metric = {
            "type": __event_type__,
            "timestamp": timestamp,
            "host": host_ip,
            "event": self.event_to_enum(data[0]),
            "vrf_id": int(data[1]),
            "src_ip": data[2],
            "x_ip": data[3],
            "start_port": int(data[4]),
            "end_port": int(data[5]),
        }
        return metric

    def event_to_enum(self, event_str: str):
        match event_str:
            case "A":
                event = NATEventTypeEnum.CREATED
            case "D":
                event = NATEventTypeEnum.DELETED
            case _:
                event = NATEventTypeEnum.CREATED
        return event
