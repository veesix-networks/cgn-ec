#
<p align="center">
  <img src="docs/img/logo.png" alt="Logo" style="max-width: 100%; height: auto;">
</p>

<a href="https://github.com/veesix-networks/cgn-ec" target="_blank">cgn-ec</a> (Event Correlation) is a super fast and flexible solution which focuses on centralizing CGNAT logging. You can view the [documentation here](https://docs.cgn-ec.veesix-networks.co.uk) and also join the [Slack](https://join.slack.com/t/cgn-ec/shared_invite/zt-2wvt40sc7-h5l3VWjYkAiZsm3uoicXww) community.

Here are some key features of this project:

- Flexible scaling with decoupled compute vs storage requirements.
- Up to 90% data compression compared to other DIY solutions.
- Up to <em>*</em>1000x faster than other enterprise solutions.
- Ability to add a new vendor within minutes.
- Flexible outputs so you can preprocess CGNAT events and ship to external systems.
- Syslog and NetFlow collectors with multi-vendor support out of the box.

![Basic Architecture](./img/veesix_networks_cgn_logging.png)

## Professional Edition

We provide support/services for this project which include maintaining the solution on-prem or via AWS and also can add new vendors/outputs if you need something developed quick.

Features included in Pro edition:

- [x] HA/Scaleout with NetFlow collector.
- [x] API Advanced Search
- [x] Cache of all active subscriber sessions
- [x] OSS/CRM Integration

If you would like a quote then please email us at [cgn-support@veesix-networks.co.uk](mailto:cgn-support@veesix-networks.co.uk).

## License

This project is licensed under <a href="https://github.com/veesix-networks/cgn-ec/blob/main/LICENSE" target="_blank">Apache License Version 2.0</a>.

### Disclaimers

<em>*</em> When using TimescaleDB output as a time-series database, you can view the [blog regarding performance here](https://www.timescale.com/blog/timescaledb-vs-amazon-timestream-6000x-higher-inserts-175x-faster-queries-220x-cheaper).