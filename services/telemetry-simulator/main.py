import json
import random
import time
from datetime import datetime, timezone
from kafka import KafkaProducer


NUM_DEVICES = 5000
EVENTS_TO_GENERATE = 10000
KAFKA_TOPIC = "telemetry-events"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"


def generate_telemetry(device_id: str) -> dict:
    is_anomaly = random.random() < 0.15

    return {
        "device_id": device_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "temperature": round(random.uniform(65, 85) if not is_anomaly else random.uniform(90, 120), 2),
        "pressure": round(random.uniform(30, 45) if not is_anomaly else random.uniform(50, 70), 2),
        "vibration": round(random.uniform(0.1, 0.6) if not is_anomaly else random.uniform(1.2, 3.0), 3),
        "voltage": round(random.uniform(210, 240) if not is_anomaly else random.uniform(180, 205), 2),
        "current": round(random.uniform(5, 12) if not is_anomaly else random.uniform(15, 25), 2),
        "rpm": round(random.uniform(1200, 1800) if not is_anomaly else random.uniform(2200, 3200), 2),
        "humidity": round(random.uniform(30, 55) if not is_anomaly else random.uniform(65, 90), 2),
        "is_anomaly_simulated": is_anomaly,
    }


def main():
    
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
        key_serializer=lambda key: key.encode("utf-8"),
        acks=1,
        retries=3,
        request_timeout_ms=10000,
        max_block_ms=10000,
    )

    print(f"Publishing {EVENTS_TO_GENERATE} telemetry events to Kafka topic '{KAFKA_TOPIC}'...")

    start = time.time()

    for _ in range(EVENTS_TO_GENERATE):
        device_id = f"device-{random.randint(1, NUM_DEVICES)}"
        event = generate_telemetry(device_id)

        producer.send(
            KAFKA_TOPIC,
            key=device_id,
            value=event,
        )

    producer.flush(timeout=10)
    producer.close()

    duration = time.time() - start
    print("\n--- Kafka Publishing Summary ---")
    print(f"Published events: {EVENTS_TO_GENERATE}")
    print(f"Simulated devices: {NUM_DEVICES}")
    print(f"Duration seconds: {duration:.2f}")
    print(f"Events/sec: {EVENTS_TO_GENERATE / duration:.2f}")


if __name__ == "__main__":
    main()