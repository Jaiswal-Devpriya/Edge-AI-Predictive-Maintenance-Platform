import json
import time
from kafka import KafkaConsumer


KAFKA_TOPIC = "telemetry-events"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
MAX_EVENTS_TO_PROCESS = 10000


def is_anomaly(event: dict) -> bool:
    return (
        event["temperature"] > 90
        or event["pressure"] > 50
        or event["vibration"] > 1.0
        or event["voltage"] < 205
        or event["current"] > 15
        or event["rpm"] > 2200
        or event["humidity"] > 65
    )


def main():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="edge-inference-service",
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    total_events = 0
    forwarded_events = 0
    dropped_events = 0

    print("Edge inference service started...")

    start = time.time()

    for message in consumer:
        event = message.value
        total_events += 1

        if is_anomaly(event):
            forwarded_events += 1
        else:
            dropped_events += 1

        if total_events >= MAX_EVENTS_TO_PROCESS:
            break

    duration = time.time() - start
    reduction = (dropped_events / total_events) * 100

    print("\n--- Edge Inference Summary ---")
    print(f"Total events processed: {total_events}")
    print(f"Forwarded anomaly events: {forwarded_events}")
    print(f"Dropped normal events: {dropped_events}")
    print(f"Cloud traffic reduction: {reduction:.2f}%")
    print(f"Duration seconds: {duration:.2f}")
    print(f"Processing throughput events/sec: {total_events / duration:.2f}")


if __name__ == "__main__":
    main()