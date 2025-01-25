# Port Mapping Creation: [timestamp] [hostname] NAT-UDP-C: 100.100.100.100:10000 -> 150.150.150.150: 10000
# Session Creation:  Tstamp AX_hostname NAT-TCP-C: fwd_src_ip:fwd_src_port<->fwd_dest_ip:fwd_dest_port, rev_src_ip:rev_src_port<-->rev_dest_ip:rev_dest_port
# Fixed-NAT: FIXED-NAT-PORTS 10.10.10.172->192.168.9.173:3000-4000

# Need to handle ASCII, COmpact and Binary logging formats
import regex as re
from typing import Any
from datetime import datetime
from structlog import get_logger

from consumer.handlers.generic import GenericSyslogHandler
from consumer.enums import NATEventTypeEnum, NATEventEnum, NATProtocolEnum

logger = get_logger("cgn-ec.handlers.a10_thunder")


class A10ThunderSyslogHandler(GenericSyslogHandler):
    TOPIC = "cgnat.syslog.a10_thunder"

    REGEX_PORT_MAPPING = r"NAT-(\w+)-(\w+): (\d+.\d+.\d+.\d+):(\d+)<-->(\d+.\d+.\d+.\d+):(\d+) to (\d+.\d+.\d+.\d+):(\d+)$"
    REGEX_SESSION_MAPPING = r"NAT-(\w+)-(\w+): (\d+.\d+.\d+.\d+):(\d+)<->(\d+.\d+.\d+.\d+):(\d+),(\d+.\d+.\d+.\d+):(\d+)<-->(\d+.\d+.\d+.\d+):(\d+)$"

    PATTERNS = [
        (re.compile(REGEX_SESSION_MAPPING), "parse_session_mapping"),
        (re.compile(REGEX_PORT_MAPPING), "parse_port_mapping"),
    ]

    def parse_port_mapping(
        self, data: tuple[str | Any], host_ip: str, timestamp: datetime
    ) -> dict:
        __event_type__ = NATEventEnum.PORT_MAPPING
        if len(data) != 8:
            return

        logger.debug("Parsing Port Mapping", data=data)
        metric = {
            "type": __event_type__,
            "timestamp": timestamp,
            "host": host_ip,
            "event": self.event_to_enum(data[1]),
            "vrf_id": 0,
            "protocol": NATProtocolEnum.from_string(data[0]),
            "src_ip": data[2],
            "src_port": int(data[3]),
            "x_ip": data[4],
            "x_port": int(data[5]),
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
            "event": self.event_to_enum(data[1]),
            "vrf_id": 0,
            "protocol": NATProtocolEnum.from_string(data[0]),
            "src_ip": data[2],
            "src_port": data[3],
            "x_ip": data[6],
            "x_port": int(data[7]),
            "dst_ip": data[4],
            "dst_port": int(data[5]),
        }
        return metric

    def event_to_enum(self, event_str: str):
        match event_str:
            case "C":
                event = NATEventTypeEnum.CREATED
            case "B":
                event = NATEventTypeEnum.CREATED
            case "D":
                event = NATEventTypeEnum.DELETED
            case "U":
                event = NATEventTypeEnum.UPDATED
            case _:
                event = NATEventTypeEnum.CREATED
        return event
