The consumer is what "consumes" the events written into Kafka, pre-processes them into a Metric which then can be handled by an output to store in a database or be sent somewhere else.

The consumer will typically implement vendor specific logic to normalize the event into one of the few Metric models available.

For example if you are looking to ingest a session mapping event from 2 CGNAT vendors but 1 represents the protocol as an integer and the other represents the protocol as a string (e.g 6 for TCP or 17 for UDP), the typical data model for a metric object requires the protocol number so you would implement some logic to transform the string to its integer equivalent.

![Consumer Basic Architecture](../img/consumer.png)

## Configuration Examples

Consumer configuration is driven via YAML or JSON. When you mount the configuration file to the consumer containers, you should set the `CONFIG_FILE` environment variable to let the consumer know where the configuration file lives.

### YAML

```yaml
# Global Configuration Settings
kafka_bootstrap_servers: "localhost:9094"
kafka_group_id: "syslog-consumers"
kafka_max_records_poll: 500
batch_size: 30000

# Handler Configuration
handler:
  type: "cgn_ec_consumer.handlers.nfware.NFWareSyslogHandler"
  options: {}

# Outputs Configuration
outputs:
  # TimeScaleDB Output
  - type: "cgn_ec_consumer.outputs.timescaledb.TimeScaleDBOutput"
    options:
      address: "tsdb"
      port: 5432
      username: "cgnat"
      password: "password123"
      database: "cgnat"
      batch_size: 30000

    # Example HTTP Output
    # - type: "HTTPWebhookOutput"
    #   options:
    #     url: "http://some-api/test"
    #     headers:
    #       x-api-key: default-change-me
    #     timeout: 10
    #   preprocessors:
    #     - name: filter_keys
    #       arguments:
    #         keys:
    #           - src_ip
    #           - src_port
    #           - x_ip
    #           - x_port
    #           - timestamp
    #           - dst_ip
    #           - dst_port
    #           - event
    #     - name: match_kvs
    #       arguments:
    #         kvs:
    #           src_ip: 192.168.3.30
    #     - name: key_exists
    #       arguments:
    #         key: dst_port
    #         ignore_none: true
```

### JSON

```json
{
  "kafka_bootstrap_servers": "localhost:9094",
  "kafka_group_id": "syslog-consumers",
  "kafka_max_records_poll": 500,
  "batch_size": 30000,
  
  "handler": {
    "type": "cgn_ec_consumer.handlers.nfware.NFWareSyslogHandler",
    "options": {}
  },
  
  "outputs": [
    {
      "type": "cgn_ec_consumer.outputs.timescaledb.TimeScaleDBOutput",
      "options": {
        "address": "tsdb",
        "port": 5432,
        "username": "cgnat",
        "password": "password123",
        "database": "cgnat",
        "batch_size": 30000
      },
      "preprocessors": [
        {
          "name": "filter_keys",
          "arguments": {
            "keys": [
              "src_ip",
              "src_port",
              "x_ip",
              "x_port",
              "timestamp",
              "dst_ip",
              "dst_port",
              "event",
              "type"
            ]
          }
        },
        {
          "name": "match_kvs",
          "arguments": {
            "kvs": {
              "src_ip": "192.168.1.20",
              "type": "session-mapping"
            }
          }
        }
      ]
    }
  ]
}
```

## Parameters

| Parameter                   | Description                           |
| --------------------------- | ------------------------------------- | 
| kafka_bootstrap_servers     | Kafka Server for consuming all events |
| kafka_group_id              | ID for the consumer group             |
| kafka_max_records_poll      | How many records are pulled           |
| config_file                 | Only set outside the configuration to reference config file path    |
| batch_size                  | TimeScaleDB Batch insert size         |
| handler.type                | Handler class for processing events   |
| handler.options             | Options passed to Handler init        |
| outputs[i].type                | Output class for processing output logic |
| outputs[i].options             | Output Options passed to Output init  |
| outputs[i].preprocessors[i].name  | Name of Preprocessor                  |
| outputs[i].preprocessors[i].arguments | Arguments passed to Preprocessor init |