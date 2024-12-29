# cgn-ec
CGN Event Correlation

This project is currently a work in progress and will be subject to change core components throughout the next few months.

![Architecture Overview](docs/img/veesix_networks_cgn_logging.png)

With this project, I aim to consolidate various methods of collecting CGNAT logs and build the architecture in a way to scale on both the ingestor side and the consumers who will process the data and pass it into external systems like an analysis tool or time-series database. The idea is that you can also enrich the data with some metadata about the CGN subscriber whether that be things like a prefix id, site id or role from your IPAM like netbox to provide quick and reliable reporting on your CGN subscribers.

TimescaleDB was initially chosen to explore the capabilities of running time series in PostgreSQL because the infrastructure can be consolidated alongside with Django/NetBox applications for my initial demos.

If you are interested in funding this project or obtaining a support contract which will allow me to develop this further and provide better support with proper SLAs, then please do reach out to me via [Veesix ::networks](https://veesix-networks.co.uk) or contact me at support[at]veesix-networks.co.uk.

```
$ curl --location 'http://localhost:8000/v1/sessions/?x_ip=194.15.97.34&x_port=39940&timestamp_gt=2024-12-29T01%3A29%3A33Z' | jq
[
  {
    "timestamp": "2024-12-29T01:30:33Z",
    "event": "A",
    "protocol": 17,
    "src_port": 50710,
    "x_ip": "194.15.97.34",
    "dst_port": 443,
    "vrf_id": 5,
    "src_ip": "100.64.23.122",
    "x_port": 39940,
    "dst_ip": "173.184.60.34",
    "direction": "OUT"
  }
]
$ curl --location 'http://localhost:8000/v1/sessions/?x_ip=194.15.97.34&timestamp_gt=2024-12-29T01%3A29%3A33Z' | jq
[
  {
    "timestamp": "2024-12-29T01:30:28Z",
    "event": "A",
    "protocol": 6,
    "src_port": 61648,
    "x_ip": "194.15.97.34",
    "dst_port": 443,
    "vrf_id": 0,
    "src_ip": "100.64.23.122",
    "x_port": 51562,
    "dst_ip": "8.205.3.117",
    "direction": "OUT"
  },
  {
    "timestamp": "2024-12-29T01:30:28Z",
    "event": "D",
    "protocol": 6,
    "src_port": 46220,
    "x_ip": "194.15.97.34",
    "dst_port": 443,
    "vrf_id": 0,
    "src_ip": "100.64.23.122",
    "x_port": 19174,
    "dst_ip": "181.48.102.136",
    "direction": "OUT"
  },
  {
    "timestamp": "2024-12-29T01:30:28Z",
    "event": "D",
    "protocol": 17,
    "src_port": 15181,
    "x_ip": "194.15.97.34",
    "dst_port": 443,
    "vrf_id": 5,
    "src_ip": "100.64.23.122",
    "x_port": 46001,
    "dst_ip": "71.153.149.89",
    "direction": "OUT"
  },
  ...
]
```