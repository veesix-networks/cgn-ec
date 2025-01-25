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

logger = get_logger("cgn-ec.handlers.f5_bigip")


class F5BIGIPSyslogHandler(GenericSyslogHandler):
    TOPIC = "cgnat.syslog.f5_bigip"

    REGEX_SESSION_MAPPING = r"(\S+) (\d+.\d+.\d+.\d+)%(\d+):(\d+) (\d+) (\d+.\d+.\d+.\d+)%\d+:(\d+) (\d+.\d+.\d+.\d+) (\d+)$"

    PATTERNS = [
        (re.compile(REGEX_SESSION_MAPPING), "parse_session_mapping"),
    ]

    def parse_session_mapping(
        self, data: tuple[str | Any], host_ip: str, timestamp: datetime
    ) -> dict:
        __event_type__ = NATEventEnum.SESSION_MAPPING
        if len(data) != 9:
            return

        logger.debug("Parsing Session Mapping", data=data)
        metric = {
            "type": __event_type__,
            "timestamp": timestamp,
            "host": host_ip,
            "event": self.event_to_enum(data[0]),
            "vrf_id": int(data[2]),
            "protocol": NATProtocolEnum(data[4]),
            "src_ip": data[1],
            "src_port": data[3],
            "x_ip": data[5],
            "x_port": int(data[6]),
            "dst_ip": data[7],
            "dst_port": int(data[8]),
        }
        return metric

    def event_to_enum(self, event_str: str):
        match event_str:
            case "LSN_ADD":
                event = NATEventTypeEnum.CREATED
            case "LSN_INBOUND_ADD":
                event = NATEventTypeEnum.CREATED
            case "LSN_DELETE":
                event = NATEventTypeEnum.DELETED
            case "LSN_INBOUND_DELETE":
                event = NATEventTypeEnum.DELETED
            case _:
                event = NATEventTypeEnum.CREATED
        return event
