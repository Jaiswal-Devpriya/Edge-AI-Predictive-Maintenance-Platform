CREATE TABLE IF NOT EXISTS anomaly_events (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(100) NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    temperature DOUBLE PRECISION,
    pressure DOUBLE PRECISION,
    vibration DOUBLE PRECISION,
    voltage DOUBLE PRECISION,
    current_value DOUBLE PRECISION,
    rpm DOUBLE PRECISION,
    humidity DOUBLE PRECISION,
    anomaly_score DOUBLE PRECISION,
    severity VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);