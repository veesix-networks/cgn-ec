The [official Python SDK](https://github.com/veesix-networks/cgn-ec-python) for CGN-EC can be installed by running `pip install cgn-ec`.

The following requirements are chosen:

- httpx
    - Sync and Async HTTP client.
- pydantic
    - Align data models with the API which also uses Pydantic. This covers basic data validation and enforces data types when data is initialized.

## How to use

### 1. Import cgn_ec API object

```py
--8<-- "docs/examples/python_sdk.py:1:1"
```

### 2. Instantiate the API with your URL and API token

```py
--8<-- "docs/examples/python_sdk.py:3:3"
```

### 3. Query the API with optional parameters

```py
--8<-- "docs/examples/python_sdk.py:5:5"
```

## Methods

- `get_session_mappings()`
- `get_address_mappings()`
- `get_port_mappings()`
- `get_port_block_mappings()`

## Notes

Methods will typically match the relevant API endpoint, for example the `/v1/port_block_mappings` API endpoint will map to `get_port_block_mappings` in the Python SDK.

Query parameters are also mapped on a 1:1 basis, so `GET /v1/session_mappings` supports parameters `x_ip, timestamp_gt, timestamp_lt, limit and skip` in the query which can be translated to:
```python
mappings = cgnec.get_session_mappings(
    x_ip="127.1.2.3",
    timestamp_gt="2024-12-29T01:29:33Z",
    timestamp_lt="2024-12-29T01:29:35Z",
    limit=10,
    skip=0
)
```