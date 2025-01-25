# https://doc.6wind.com/turbo-router-3.x/user-guide/cli/ip-networking/cgnat.html#events
# Session Mapping:      Jun 14 12:17:35 dut-vm fp-cgnat[2484]: NEW CONN: fwd proto 6 10.100.0.1:4241 -> 10.200.0.1:33815, back proto 6 10.200.0.1:33815 --> 10.175.0.3:10752
#                       Jun 14 12:19:04 dut-vm fp-cgnat[2484]: DESTROY CONN: fwd proto 6 10.100.0.1:4241 -> 10.200.0.1:33815, back proto 6 10.200.0.1:33915 -> 10.175.0.3:10753
# Port Block Mapping:   Jun 11 08:02:46 vsr fp-cgnat[4269]: CGNAT Log listen on 5001
#                       Jun 11 08:03:09 vsr fp-cgnat[4269]: USER 100.64.0.1 (matching rule 1): NEW BLOCK (pool "mypool", ip public 192.0.2.33, proto 6, port 1 - 512)
#                       Jun 11 08:07:30 vsr fp-cgnat[4269]: USER 100.64.0.1 (matching rule 1): DESTROY BLOCK (pool "mypool", ip public 192.0.2.33, proto 6, port 1 - 512)

import re
from datetime import datetime
from structlog import get_logger

from consumer.handlers.generic import BaseSyslogHandler
from consumer.models import (
    MetricBase,
    NATSessionMapping,
    NATPortBlockMapping,
)
from consumer.enums import NATEventTypeEnum


logger = get_logger("cgn-ec.handlers.sixwind")


class SixWindSyslogHandler(BaseSyslogHandler):
    TOPIC = "cgnat.syslog.sixwind"

    REGEX_SESSION_MAPPING = r"^fp-cgnat\[\d+\]: (?P<event>NEW CONN|DESTROY CONN): fwd proto (?P<protocol>\d+) (?P<src_ip>\d+\.\d+\.\d+\.\d+):(?P<src_port>\d+) -> (?P<x_ip>\d+\.\d+\.\d+\.\d+):(?P<x_port>\d+), back proto \d+ \d+\.\d+\.\d+\.\d+:\d+ --> (?P<dst_ip>\d+\.\d+\.\d+\.\d+):(?P<dst_port>\d+)$"
    REGEX_PORT_BLOCK_MAPPING = r"^(?P<event>[A|D]) VRF (?P<vrf_id>\d+) INT (?P<src_ip>\d+\.\d+\.\d+\.\d+) EXT (?P<x_ip>\d+\.\d+\.\d+\.\d+):(?P<start_port>\d+)-(?P<end_port>\d+)$"

    PATTERNS = {
        REGEX_SESSION_MAPPING: "parse_session_mapping",
        REGEX_PORT_BLOCK_MAPPING: "parse_port_block_mapping",
    }

    def parse_message(self, data: dict) -> MetricBase:
        syslog_message = data["message"]
        timestamp = data["timestamp"]

        for pattern, parse_func in self.PATTERNS.items():
            has_match = re.search(pattern, syslog_message)
            if not has_match:
                continue

            parse_method = getattr(self, parse_func)
            event_data = has_match.groupdict()

            result = parse_method(event_data, timestamp)
            return result

        logger.debug("Could not find a valid regex pattern to parse syslog message")

    def parse_session_mapping(
        self, data: dict, timestamp: datetime
    ) -> NATSessionMapping:
        logger.debug("Parsing Session Mapping", data=data)
        metric = NATSessionMapping(
            timestamp=timestamp,
            event=self.event_to_enum(data["event"]),
            protocol=int(data["protocol"]),
            src_ip=data["src_ip"],
            src_port=data["src_port"],
            x_ip=data["x_ip"],
            x_port=int(data["x_port"]),
            dst_ip=data["dst_ip"],
            dst_port=int(data["dst_port"]),
        )
        return metric

    def parse_port_block_mapping(
        self, data: dict, timestamp: datetime
    ) -> NATPortBlockMapping:
        logger.debug("Parsing Port Block Mapping", data=data)

    def event_to_enum(self, event_str: str):
        match event_str:
            case "NEW CONN":
                event = NATEventTypeEnum.CREATED
            case "DESTROY CONN":
                event = NATEventTypeEnum.DELETED
            case _:
                event = NATEventTypeEnum.CREATED
        return event
