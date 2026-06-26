import json
import random
import time
from datetime import datetime, timezone


NUM_DEVICES = 5000
EVENTS_TO_GENERATE = 10000


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
    print(f"Starting telemetry simulator for {NUM_DEVICES} devices...")

    start = time.time()

    for i in range(EVENTS_TO_GENERATE):
        device_id = f"device-{random.randint(1, NUM_DEVICES)}"
        event = generate_telemetry(device_id)

        print(json.dumps(event))

    duration = time.time() - start
    print("\n--- Simulation Summary ---")
    print(f"Generated events: {EVENTS_TO_GENERATE}")
    print(f"Simulated devices: {NUM_DEVICES}")
    print(f"Duration seconds: {duration:.2f}")
    print(f"Events/sec: {EVENTS_TO_GENERATE / duration:.2f}")


if __name__ == "__main__":
    main()