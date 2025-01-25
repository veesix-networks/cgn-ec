The API for cgn-ec provides basic capabilities to lookup in the timescaledb tables, currently this is the only supported feature to fetch data from.

It's advised to only query with a +- 1 second range in the timestamp (lt and gt) otherwise for large datasets you API could become slow. You should also factor in when you are recieving a DPA request from the police that the timestamp information is accurate and only has minimal error in the ranges.

If you would like to query the database more frequently and configure your own reporting instead of using the pro edition, we would advise you to use timescaledb continuous aggregates and develop a new endpoint for reporting instead of directly using the main API endpoints, below you can browse the OpenAPI schema for cgn-ec.

<redoc src="./openapi.json"/>