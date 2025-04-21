API hooks allow you to enrich the API response data.

If you would like to send an external API call to your CRM or an external system like a RADIUS database to perform a query based on a specific metric field (eg. `src_ip`), then you can implement your own hook to achieve this.

Let's say we want to query our RADIUS accounting server to find a specific `src_ip` for a given timestamp and retrieve the DHCP remote-id, and then query our CRM for this remote-id to get the subscriber specific details:

1) Create a `hooks` folder so we can mount this to our `cgn-ec` API application.

```sh
mkdir hooks
```

2) Mount the hooks folder into the API container.

```sh
services:
  api:
    volumes:
      - ./hooks:/hooks
```

3) Create your hook file that contains your logic. There are 4 hooks you can implement: `session_mapping_hook`, `address_mapping_hook`, `port_mapping_hook` and `port_block_mapping_hook`.

`./hooks/populate_radius.py`
```python
from cgn_ec_api.models.generic import (
    NATSessionMappingRead,
    HookMetadata,
)

def session_mapping_hook(event: NATSessionMappingRead) -> None:
    event.hook_metadata = HookMetadata(
        data=get_radius_accounting(event)
    )
```

4) Reference the `populate_radius` hook in your API call using the `?hook=<name>` query parameter:

```sh
curl -X 'GET' \
  'http://localhost:3001/v1/session_mappings/?limit=100&skip=0&timestamp_ge=2025-01-25T05%3A08%3A53Z&hook=populate_radius' \
  -H 'accept: application/json' \
  -H 'x-api-key: default-change-me'
```

```json
[
 {
   "timestamp": "2025-01-25T05:08:53.465000Z",
   "hook_metadata": {
     "data": {
       "ip": "100.64.23.122",
       "circuit_id": "OLT-123 - PON13 - ONU94 - Eth1",
       "remote_id": "e6820bfd-aeed-49c9-81a1-0796a8a02f5a"
     },
     "error": null
   },
   "host": "172.18.0.1",
   "event": 2,
   "vrf_id": 0,
   "protocol": 6,
   "src_ip": "100.64.23.122",
   "src_port": 1738,
   "x_ip": "194.15.97.34",
   "x_port": 21288,
   "dst_ip": "187.104.134.22",
   "dst_port": 443
 }
]

```