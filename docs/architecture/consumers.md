The consumer is what "consumes" the events written into Kafka, pre-processes them into a Metric which then can be handled by an output to store in a database or be sent somewhere else.

The consumer will typically implement vendor specific logic to normalize the event into one of the few Metric models available.

For example if you are looking to ingest a session mapping event from 2 CGNAT vendors but 1 represents the protocol as an integer and the other represents the protocol as a string (e.g 6 for TCP or 17 for UDP), the typical data model for a metric object requires the protocol number so you would implement some logic to transform the string to its integer equivalent.

![Consumer Basic Architecture](../img/consumer.png)