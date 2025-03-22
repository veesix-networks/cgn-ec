TimescaleDB is our preferred Output of choice when storing your CGNAT logs in a time-series database.

A lot of effort has gone into the data modelling and figuring out the right compression policies to get the most out of the underlying storage.

You can view the data models [here on the GitHub repository](https://github.com/veesix-networks/cgn-ec-models/blob/main/cgn_ec_models/sqlmodel.py)

These data models can also be used in other databases but you will need to translate the model to the relevant format, eg. using the influx line protocol when using influxdb.

The 4 main models are as followed:

- `NATSessionMapping`
    - Typically describes a CGNAT Subscriber session with a translated IP and port (aka Port Address Translation / PAT)
- `NATAddressMapping`
    - Typically describes a CGNAT 1:1 translation
- `NATPortMapping`
    - Typically describes the same as a `NATSessionMapping` but excluding the destination IP and port
- `NATPortBlockMapping`
    - Typically describes a port block assosication (typically referred as Port Block Allocation / PBA )

All of these models inherit the base `MetricBase`, an output should ideally implement logic to handle all 4 of these data models when requested to process a metric.