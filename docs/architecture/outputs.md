An output is an implementation to send the processed event to an external system, like a database, back into Kafka or for example a HTTP endpoint.

Outputs must only process metrics and not perform any processing steps to change the data. Outputs are designed to work with any handler type so it doesn't matter what vendor or data you are ingesting, the output will work regardless.

![Output Architecture](../img/output.png)

## Supported Outputs

### TimescaleDB

Time-series based database built around PostGRES. This is our preferred output when storing long lived data due to the compression techniques used to be able to store the most amount of logs and is a validated design.

### HTTP

HTTP based webhook where you can configure specific matches (eg. on a certain x_ip) and send a HTTP request to a configured endpoint.

## Preprocessors

Preprocessors can be attached to an output to perform logic such as filtering specific keys or checking a certain key/value pair exist. Here are some scenarios where you could apply a preprocessor to a relevant output:

- You need to filter a few fields and specifically target a `src_ip` of `100.64.22.13` and the `dst_port` field must exist, then send this to a HTTP API for further processing. In this scenario you can use the `HTTPWebhookOutput` output combined with the `filter_keys`, `match_kvs` and `key_exists` preprocessors.
- You need to send events for a specific `src_ip` to a Kafka queue for further processing. In this scenario you can use the `KafkaOutput` output combined with the `match_kvs` preprocessor.
- You need to temporarily drop any metrics with a specific `dst_ip` and `dst_port`. You can use the `BlackholeOutput` output combined with the `match_kvs` preprocessor.

You can view [more details on preprocessors here](./preprocessors.md).