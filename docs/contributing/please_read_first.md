# Contributing

When contributing to this project, please first discuss the change you wish to make via GitHub discussions, an issue or an informal option such as the Slack community.

We don't currently have a dedicated code of conduct however, it is expected that you treat everyone with respect in the community.

Any feedback for the contributing workflows whether it be the branch structure, coding style, tests or general feedback of the implementation is welcome and should be brought up either as a discussion/issue or informally over a chat like Slack. Do not use emails/GitHub Issues for informal discussions.

## Dev Setup

`docker-compose-local.yml` is typically used to stand up a basic cgn-ec infrastructure including the timescale database and kafka queue. If you are developing for a specific producer/consumer then it is advised to pull in the repo locally and change the build process to use context and Dockerfile instead of using the `image` tag under the service.

### Ports

| Container         | Host Port / Container Port    | Purpose                  |
| -----------       | -----                         | ------------------------------------  |
| syslog_collector  | 1514:1514/udp                 | Syslog collector/producer             |
| netflow_collector | 9995:9995/udp                 | NetFlow collector/producer            |
| kafka             | 9094:9094/tcp                 | Kafka message queue for collectors    |
| kafka-ui          | 8080:8080/tcp                 | UI for Kafka                          |
| db                | 5432:5432/tcp                 | TimeScaleDB for CGN metrics           |
| consumer          | N/A                           | Python Consumer                       |
| prometheus        | 9090:9090/tcp                 | Collects Kafka and Collector perf.    |
| grafana           | 3000:3000/tcp                 | Dashboard for perf. metrics           |
| kafka-exporter    | N/A                           | Kafka Prometheus Exporter             |
| api               | 3001:80/tcp                   | cgn-ec API for the TimeScaleDB        |
