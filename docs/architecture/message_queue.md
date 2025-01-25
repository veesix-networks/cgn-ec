Kafka is a distributed event streaming platform used in the cgn-ec ecosystem to centralize the ingestion of all events.

This ensures a common entrypoint for all the data from the 3 currently supported methods:

- Syslog
- NetFlow
- RADIUS Accounting

Consumers then tap into the kafka infrastructure, ensuring the initial logic of gathering the data is the same across any vendor or device type, handlers are what then perform the low-level logic like regex parsing, data transformation and data type normalization before passing the parsed metric to an output.

Without Kafka, we don't normalize the initial entrypoint for data and then various implementations become unmaintainable at a later stage in the development cycle. We want all consumers to be as close as possible in terms of ingesting the initial event, there is no doubt that various vendors will need different low level logic to parse the messages but if we can create a standard ingestion pattern across any vendor and transport type, then the vendor specific handlers become practical for anyone with little to no python knowledge.

If you already are using Kafka in production, then its as easy as creating a new topic with the optimal amount of partitions based on how many CGNAT sessions/event flows you want to ingest. If you have never ran it before, then you can initially use the provided implementation in the [docker compose file found on our GitHub repository](https://github.com/veesix-networks/cgn-ec/blob/main/docker-compose.yml) to get started.

For most setups, you don't need to tweak the base configuration options on Kafka other than configuring the right amount of partitions.

You can visit the Apache of Confluent websites to view more details and documentation on this, however the golden rule is typically `# of partitions = # of consumers` with a high limit of around 15+ partitions. 

Depending on some configurations if you would prefer redundancy over latency within a failover scenario, it's advised to setup a dedicated Kafka cluster and manage that separately as apart of the cgn-ec infrastructure.