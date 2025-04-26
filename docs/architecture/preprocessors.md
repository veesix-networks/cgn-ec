A preprocessor is a piece of logic attached to an output, which runs prior to processing the metrics. Some examples would include filtering specific keys on a metric or matching a specific key/value pair.

## Generic preprocessors

### filter_keys

Filters a metric for specific keys and only returns those keys specified.

```yaml title="config.yaml" hl_lines="9-20"
  # Example HTTP Output
  outputs:
  - type: "HTTPWebhookOutput"
    options:
      url: "http://10.4.21.133:3013/test"
      headers:
        x-api-key: default-change-me
      timeout: 10
    preprocessors:
      - name: filter_keys
        arguments:
          keys:
            - src_ip
            - src_port
            - x_ip
            - x_port
            - timestamp
            - dst_ip
            - dst_port
            - event
```

### match_kv

Filters metrics that only match the specific key/value pair.

```yaml title="config.yaml" hl_lines="9-13"
  # Example HTTP Output
  outputs:
  - type: "HTTPWebhookOutput"
    options:
      url: "http://10.4.21.133:3013/test"
      headers:
        x-api-key: default-change-me
      timeout: 10
    preprocessors:
      - name: match_kv
        arguments:
          key: src_ip
          value: 100.64.22.31
```

### match_kvs

Like `match_kv`, but allows you to match multiple key/value pairs. If one doesn't exist then the metric is dropped.

```yaml title="config.yaml" hl_lines="9-14"
  # Example HTTP Output
  outputs:
  - type: "HTTPWebhookOutput"
    options:
      url: "http://10.4.21.133:3013/test"
      headers:
        x-api-key: default-change-me
      timeout: 10
    preprocessors:
      - name: match_kvs
        arguments:
          kvs:
            src_ip: 100.64.22.31
            dst_port: 443
```

### key_exists

Filters metrics that have a specific key. By default, if the key value is `None`, the metric is dropped. Override this behaviour by setting `ignore_none` to true.

```yaml title="config.yaml" hl_lines="9-13"
  # Example HTTP Output
  outputs:
  - type: "HTTPWebhookOutput"
    options:
      url: "http://10.4.21.133:3013/test"
      headers:
        x-api-key: default-change-me
      timeout: 10
    preprocessors:
      - name: key_exists
        arguments:
          key: dst_port
          ignore_none: true
```