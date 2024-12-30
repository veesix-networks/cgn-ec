Here are our recommendations for production to run cgn-ec.

## Hardware Requirements

- Separate PostGRES database with multi-core, lots of memory and SSDs.
- Docker or Kubernetes infrastructure to scale the collectors and consumers.
- Dedicated CPU core (more cores is better for the consumers/data processors).
- If running a dedicated Kafka setup, follow hardware recommendations with ZooKeeper or KRaft configuration.

!!! question "Don't want to worry about the infrastructure?"
    If you don't want to worry about the hardware requirements, we can host the infrastructure for you under an enterprise license.

## Collectors

A collector is a container which implements the various logic to pass messages into Kafka so they can be normalized by a consumer. Collectors should be as simple as possible, take a look at the syslog-ng and nfacctd (NetFlow) collectors.

- Load Balancer infront of multiple collectors to scale out ingestion.
- Separate Collector per collection method, eg. 1 syslog collector and 1 netflow collector. (You can install both on the same VM if you don't want to use containers but this is not a supported method).

## Consumers

A consumer consumes messages from a Kafka topic. This then pre-processes the data into a relevant metric that can be passed to an output (for example, sending a specific event to a webhook or storing the data in the TimescaleDB).

A consumer implements a handler class which typically is created per-vendor. It is recommended that you run 2 separate consumers if you are ingesting both syslog and netflow data.

When a consumer can not handle the load of the data being collected, you can scale out the consumers by either spinning up a new docker container or using an automatic scaleout feature in your container orchestrator (eg. Horiziontal Pod Auto-Scaler with Kubernetes).