from cgn_ec.api import API

cgnec = API("https://cgn-ec.your-domain.com", "default-change-me")

mappings = cgnec.get_session_mappings(timestamp_gt="2024-12-29T01:29:33Z")
print(mappings)
"""
[
    NATSessionMapping(
        timestamp=datetime.datetime(2025, 1, 25, 5, 8, 53, 465000, tzinfo=TzInfo(UTC)),
        host=IPv4Address('172.18.0.1'),
        event=<NATEventTypeEnum.DELETED: 2>,
        vrf_id=0,
        protocol=6,
        src_ip=IPv4Address('100.64.23.122'),
        src_port=1738,
        x_ip=IPv4Address('194.15.97.34'),
        x_port=21288,
        dst_ip=IPv4Address('187.104.134.22'),
        dst_port=443
    ),
    NATSessionMapping(
        timestamp=datetime.datetime(2025, 1, 25, 5, 8, 53, 364000, tzinfo=TzInfo(UTC)),
        host=IPv4Address('172.18.0.1'),
        event=<NATEventTypeEnum.CREATED: 1>,
        vrf_id=0,
        protocol=17,
        src_ip=IPv4Address('100.64.23.122'),
        src_port=45562,
        x_ip=IPv4Address('194.15.97.34'),
        x_port=9108,
        dst_ip=IPv4Address('14.203.19.99'),
        dst_port=443
    )
]
"""
