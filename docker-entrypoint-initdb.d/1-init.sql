-- Connect to the default database (usually postgres or defaultdb)
\connect postgres;

-- Create the 'cgnat' database
-- CREATE DATABASE cgnat;

-- Connect to the 'cgnat' database
\connect cgnat
CREATE EXTENSION IF NOT EXISTS timescaledb;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO cgnat;

CREATE TABLE address_mapping (
        timestamp TIMESTAMPTZ NOT NULL,
        host INET NOT NULL,
        event SMALLINT NOT NULL, 
        vrf_id VARCHAR, 
        src_ip INET NOT NULL, 
        x_ip INET NOT NULL
);

CREATE TABLE port_block_mapping (
        timestamp TIMESTAMPTZ NOT NULL, 
        host INET NOT NULL,
        event SMALLINT NOT NULL, 
        vrf_id VARCHAR, 
        src_ip INET NOT NULL, 
        x_ip INET NOT NULL, 
        start_port INTEGER NOT NULL, 
        end_port INTEGER NOT NULL
);

CREATE TABLE port_mapping (
        timestamp TIMESTAMPTZ NOT NULL,
        host INET NOT NULL,
        event SMALLINT NOT NULL, 
        vrf_id VARCHAR, 
        protocol SMALLINT NOT NULL, 
        src_ip INET NOT NULL, 
        src_port INTEGER, 
        x_ip INET NOT NULL, 
        x_port INTEGER NOT NULL
);

CREATE TABLE session_mapping (
        timestamp TIMESTAMPTZ NOT NULL,
        host INET NOT NULL,
        event INTEGER NOT NULL, 
        vrf_id VARCHAR, 
        protocol SMALLINT, 
        src_ip INET NOT NULL, 
        src_port INTEGER NOT NULL, 
        x_ip INET, 
        x_port INTEGER, 
        dst_ip INET NOT NULL, 
        dst_port INTEGER NOT NULL
);

SELECT create_hypertable('session_mapping', by_range('timestamp', INTERVAL '1 hour'));
SELECT create_hypertable('address_mapping', by_range('timestamp', INTERVAL '1 hour'));
SELECT create_hypertable('port_mapping', by_range('timestamp', INTERVAL '1 hour'));
SELECT create_hypertable('port_block_mapping', by_range('timestamp', INTERVAL '1 hour'));

ALTER TABLE session_mapping SET (timescaledb.compress, timescaledb.compress_orderby = 'timestamp DESC', timescaledb.compress_segmentby = 'x_ip');
ALTER TABLE address_mapping SET (timescaledb.compress, timescaledb.compress_orderby = 'timestamp DESC', timescaledb.compress_segmentby = 'x_ip');
ALTER TABLE port_mapping SET (timescaledb.compress, timescaledb.compress_orderby = 'timestamp DESC', timescaledb.compress_segmentby = 'x_ip');
ALTER TABLE port_block_mapping SET (timescaledb.compress, timescaledb.compress_orderby = 'timestamp DESC', timescaledb.compress_segmentby = 'x_ip');

SELECT add_compression_policy('session_mapping', compress_after => INTERVAL '1d');
SELECT add_compression_policy('address_mapping', compress_after => INTERVAL '1d');
SELECT add_compression_policy('port_mapping', compress_after => INTERVAL '1d');
SELECT add_compression_policy('port_block_mapping', compress_after => INTERVAL '1d');