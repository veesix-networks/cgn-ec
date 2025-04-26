Here are our recommendations for production to run cgn-ec.

- Separate PostGRES database with multi-core, lots of memory and SSDs.
- Docker or Kubernetes infrastructure to scale the collectors and consumers.
- Dedicated CPU cores (more cores is better for the consumers/data processors).
- If running a dedicated Kafka setup, follow hardware recommendations with ZooKeeper or KRaft configuration.
- 1 CPU core for every 30,000 Kafka messages ratio for a consumer is good for very basic pre-processing flows. However this can change depending on how efficient you build the Handler code or which outputs you enable.

For a realistic deployment, you'll probably configure at least 1 handler, 1 output and run over the network which adds a slight extra delay to fetching records from the message queue and sending the metrics to the output, therefore you should aim for around 5k messages per second, per vCPU.

!!! question "Don't want to worry about the infrastructure?"
    If you don't want to worry about the hardware requirements, we can host the infrastructure for you under a pro license.

## Collectors

A collector is a container which implements the various logic to pass messages into Kafka so they can be normalized by a consumer. Collectors should be as simple as possible, take a look at the syslog-ng, freeradius (RADIUS Accounting) and nfacctd (NetFlow) collectors. Here are some basic scaling recommendations:

- Load Balancer infront of multiple collectors to scale out ingestion.
- Separate Collector per collection method, eg. 1 syslog collector and 1 netflow collector. (You can install both on the same VM if you don't want to use containers but this is not a supported method).
- Only collect what you need to process. (eg. performing specific regex matches on a syslog message on the collector side.)

## Consumers

A consumer consumes messages from a Kafka topic. This then pre-processes the data into a relevant metric that can be passed to an output (for example, sending a specific event to a webhook or storing the data in the TimescaleDB).

A consumer implements a handler class which typically is created per-vendor. It is recommended that you run separate consumers if you are ingesting various methods such as RADIUS Accounting, Syslog and NetFlow.

When a consumer can not handle the load of the data being collected, you can scale out the consumers by either spinning up a new docker container or using an automatic scaleout feature in your container orchestrator (eg. Horiziontal Pod Auto-Scaler with Kubernetes). Ensure you partition your kafka topics according to the amount of consumers for the specific topic.