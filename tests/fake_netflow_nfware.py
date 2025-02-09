from scapy.all import *
from scapy.layers.netflow import *
import random
import time


def random_ipv4():
    ip = f"{random.randint(100, 200)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
    return ip


def random_port():
    return random.randint(1024, 65535)


header = (
    Ether(dst="00:0c:29:fa:46:d1")
    / IP(dst="10.4.21.133")
    / UDP(sport=random_port(), dport=9995)
)
netflow_header = NetflowHeader() / NetflowHeaderV9()

flowset = NetflowFlowsetV9(
    templates=[
        NetflowTemplateV9(
            template_fields=[
                NetflowTemplateFieldV9(fieldType=323, fieldLength=8),  # timeStamp
                NetflowTemplateFieldV9(fieldType=8, fieldLength=4),  # sourceIPv4Address
                NetflowTemplateFieldV9(
                    fieldType=225, fieldLength=4
                ),  # postNATSourceIPv4Address
                NetflowTemplateFieldV9(
                    fieldType=4, fieldLength=1
                ),  # protocolIdentifier
                NetflowTemplateFieldV9(
                    fieldType=7, fieldLength=2
                ),  # sourceTransportPort
                NetflowTemplateFieldV9(
                    fieldType=227, fieldLength=2
                ),  # postNAPTSourceTransportPort
                NetflowTemplateFieldV9(
                    fieldType=12, fieldLength=4
                ),  # destinationIPv4Address
                NetflowTemplateFieldV9(
                    fieldType=226, fieldLength=4
                ),  # postNATDestinationIPv4Address
                NetflowTemplateFieldV9(
                    fieldType=11, fieldLength=2
                ),  # destinationTransportPort
                NetflowTemplateFieldV9(
                    fieldType=228, fieldLength=2
                ),  # postNAPTDestinationTransportPort
                NetflowTemplateFieldV9(
                    fieldType=229, fieldLength=1
                ),  # natOriginatingAddressRealm
                NetflowTemplateFieldV9(fieldType=234, fieldLength=4),  # ingressVRFID
                NetflowTemplateFieldV9(fieldType=230, fieldLength=1),  # natEvent
            ],
            templateID=256,
            fieldCount=13,
        )
    ],
    flowSetID=0,
)

recordClass = GetNetflowRecordV9(flowset)

dataFS = NetflowDataflowsetV9(
    templateID=256,
    records=[
        recordClass(
            observationTimeMilliseconds=int(time.time() * 1000),
            IPV4_SRC_ADDR=random_ipv4(),
            postNATSourceIPv4Address=random_ipv4(),
            PROTOCOL=random.choice([6, 17]),
            L4_SRC_PORT=random_port(),
            postNAPTSourceTransportPort=random_port(),
            IPV4_DST_ADDR=random_ipv4(),
            postNATDestinationIPv4Address=random_ipv4(),
            L4_DST_PORT=random_port(),
            postNAPTDestinationTransportPort=random_port(),
            natOriginatingAddressRealm=random.choice([0, 1]),
            ingressVRFID=random.randint(1, 1000),
            natEvent=random.choice([1, 2, 3, 4]),
        )
        for _ in range(10)
    ],
)

iface = conf.route.route("10.4.21.133")[0]
pkt = header / netflow_header / flowset / dataFS

sendp(pkt, iface=iface)
