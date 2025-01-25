An output is an implementation to send the processed event to an external system, like a database, back into Kafka or for example a HTTP endpoint.

Outputs must only process metrics and not perform any processing steps to change the data. Outputs are designed to work with any handler type so it doesn't matter what vendor or data you are ingesting, the output will work regardless.

![Output Architecture](../img/output.png)

## Supported Outputs

### TimescaleDB

Time-series based database built around PostGRES. This is our preferred output when storing long lived data due to the compression techniques used to be able to store the most amount of logs and is a validated design.

### HTTP

HTTP based webhook where you can configure specific matches (eg. on a certain x_ip) and send a HTTP request to a configured endpoint.