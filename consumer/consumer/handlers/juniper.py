# https://docs.nfware.com/en/6.3/nat/logging.html#message-format
# Session create: RT_FLOW - RT_FLOW_SESSION_CREATE [source-address="10.0.10.10" source-port="46776" destination-address="1.2.84.162" destination-port="80" connection-tag="0" service-name="junos-http" nat-source-address="1.2.84.172" nat-source-port="53328" nat-destination-address="1.2.84.162" nat-destination-port="80" nat-connection-tag="0" src-nat-rule-type="source rule" src-nat-rule-name="untrust" dst-nat-rule-type="N/A" dst-nat-rule-name="N/A" protocol-id="6" policy-name="permit" source-zone-name="trust" destination-zone-name="untrust" session-id="92317" username="N/A" roles="N/A" packet-incoming-interface="ge-0/0/0.0" application="UNKNOWN" nested-application="UNKNOWN" encrypted="UNKNOWN" application-category="N/A" application-sub-category="N/A" application-risk="-1" application-characteristics="N/A" src-vrf-grp="N/A" dst-vrf-grp="N/A" tunnel-inspection="Off" tunnel-inspection-policy-set="root"]
# Session close: RT_FLOW - RT_FLOW_SESSION_CLOSE [reason="TCP FIN" source-address="10.0.10.2" source-port="63996" destination-address="1.2.84.162" destination-port="80" connection-tag="0" service-name="junos-http" nat-source-address="1.2.84.169" nat-source-port="4986" nat-destination-address="1.2.84.162" nat-destination-port="80" nat-connection-tag="0" src-nat-rule-type="source rule" src-nat-rule-name="untrust" dst-nat-rule-type="N/A" dst-nat-rule-name="N/A" protocol-id="6" policy-name="permit" source-zone-name="trust" destination-zone-name="untrust" session-id="178" packets-from-client="663496" bytes-from-client="34501936" packets-from-server="719792" bytes-from-server="1079262436" elapsed-time="249" application="UNKNOWN" nested-application="UNKNOWN" username="N/A" roles="N/A" packet-incoming-interface="ge-0/0/0.0" encrypted="UNKNOWN" application-category="N/A" application-sub-category="N/A" application-risk="-1" application-characteristics="N/A" secure-web-proxy-session-type="NA" peer-session-id="0" peer-source-address="0.0.0.0" peer-source-port="0" peer-destination-address="0.0.0.0" peer-destination-port="0" hostname="NA NA" src-vrf-grp="N/A" dst-vrf-grp="N/A" tunnel-inspection="Off" tunnel-inspection-policy-set="root" session-flag="0"]
# PBA Allocate: RT_NAT - RT_SRC_NAT_PBA_ALLOC [internal-ip="10.0.10.10" block-used="1" block-max-per-host="4" block-port-low="48640" block-port-high="48895" reflexive-ip="1.2.84.172" nat-pool-name="guest" logical-system-id="0" epoch-time-64="624b0492"]
# PBA Interim: RT_NAT - RT_SRC_NAT_PBA_INTERIM [internal-ip="10.0.10.10" block-used="1" block-max-per-host="4" block-port-low="48640" block-port-high="48895" reflexive-ip="1.2.84.172" nat-pool-name="guest" logical-system-id="0" epoch-time-64="624b0492"]
# PBA Release: RT_NAT - RT_SRC_NAT_PBA_RELEASE [internal-ip="10.0.10.10" block-used="0" block-max-per-host="4" block-port-low="48640" block-port-high="48895" reflexive-ip="1.2.84.172" nat-pool-name="guest" logical-system-id="0" epoch-time-64="624b0cc7"]

from datetime import datetime
from structlog import get_logger

from consumer.handlers.generic import BaseSyslogHandler
from consumer.enums import NATEventTypeEnum, NATEventEnum


logger = get_logger("cgn-ec.handlers.juniper_junos")


class JuniperJUNOSSyslogHandler(BaseSyslogHandler):
    TOPIC = "cgnat.syslog.juniper_junos"

    def parse_message(self, data: dict) -> dict:
        syslog_message = data["message"]
        timestamp = data["timestamp"]

        parse_method = None
        kvs = self.parse_log_kv(syslog_message)
        if not kvs:
            return

        if "RT_FLOW_SESSION_CREATE" in syslog_message:
            parse_method = self.parse_session_mapping_create
        elif "RT_FLOW_SESSION_CLOSE" in syslog_message:
            parse_method = self.parse_session_mapping_close

        result = parse_method(kvs, timestamp)
        return result

    def parse_session_mapping_create(self, data: dict, timestamp: datetime) -> dict:
        __event_type__ = NATEventEnum.SESSION_MAPPING

        logger.debug("Parsing Session Mapping", data=data)
        metric = {
            "type": __event_type__,
            "timestamp": timestamp,
            "event": NATEventTypeEnum.CREATED,
            "vrf_id": 0,
            "protocol": int(data["protocol-id"]),
            "src_ip": data["source-address"],
            "src_port": int(data["source-port"]),
            "x_ip": data["nat-source-address"],
            "x_port": int(data["nat-destination-address"]),
            "dst_ip": data["destination-address"],
            "dst_port": int(data["destination-port"]),
        }
        return metric

    def parse_session_mapping_close(self, data: dict, timestamp: datetime) -> dict:
        __event_type__ = NATEventEnum.SESSION_MAPPING

        logger.debug("Parsing Session Mapping", data=data)
        metric = {
            "type": __event_type__,
            "timestamp": timestamp,
            "event": NATEventTypeEnum.DELETED,
            "vrf_id": 0,
            "protocol": int(data["protocol-id"]),
            "src_ip": data["source-address"],
            "src_port": int(data["source-port"]),
            "x_ip": data["nat-source-address"],
            "x_port": int(data["nat-destination-address"]),
            "dst_ip": data["destination-address"],
            "dst_port": int(data["destination-port"]),
        }
        return metric

    def parse_log_kv(log_message: str) -> dict:
        if "[" not in log_message and "]" not in log_message:
            return

        kv_part = log_message[log_message.index("[") + 1 : log_message.index("]")]
        kv_pairs = kv_part.split()
        kv_dict = {}

        for pair in kv_pairs:
            if "=" in pair:
                key, value = pair.split("=", 1)
                kv_dict[key.strip()] = value.strip().strip('"')

        return kv_dict
