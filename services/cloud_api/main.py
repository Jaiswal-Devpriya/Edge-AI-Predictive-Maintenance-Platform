import json
from datetime import datetime

import psycopg2
import redis
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="Edge AI Predictive Maintenance Cloud API")

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

db_conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="predictive_maintenance",
    user="edgeai",
    password="edgeai",
)


class AnomalyEvent(BaseModel):
    device_id: str
    timestamp: str
    temperature: float
    pressure: float
    vibration: float
    voltage: float
    current: float
    rpm: float
    humidity: float
    anomaly_score: float = 1.0
    severity: str = "critical"


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/anomalies")
def create_anomaly(event: AnomalyEvent):
    cursor = db_conn.cursor()

    cursor.execute(
        """
        INSERT INTO anomaly_events (
            device_id,
            event_timestamp,
            temperature,
            pressure,
            vibration,
            voltage,
            current_value,
            rpm,
            humidity,
            anomaly_score,
            severity
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            event.device_id,
            datetime.fromisoformat(event.timestamp.replace("Z", "+00:00")),
            event.temperature,
            event.pressure,
            event.vibration,
            event.voltage,
            event.current,
            event.rpm,
            event.humidity,
            event.anomaly_score,
            event.severity,
        ),
    )

    db_conn.commit()
    cursor.close()

    redis_client.set(
        f"device:{event.device_id}:latest_anomaly",
        json.dumps(event.model_dump()),
        ex=3600,
    )

    return {
        "status": "stored",
        "device_id": event.device_id,
        "severity": event.severity,
    }