import json
import time
import numpy as np
import onnxruntime as ort
from kafka import KafkaConsumer


KAFKA_TOPIC = "telemetry-events"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
MODEL_PATH = "models/anomaly_detector.onnx"
MAX_EVENTS_TO_PROCESS = 10000


def event_to_features(event: dict) -> np.ndarray:
    return np.array([[
        event["temperature"],
        event["pressure"],
        event["vibration"],
        event["voltage"],
        event["current"],
        event["rpm"],
        event["humidity"],
    ]], dtype=np.float32)


def main():
    session = ort.InferenceSession(MODEL_PATH)
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="edge-inference-onnx-service",
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    )

    total_events = 0
    forwarded_events = 0
    dropped_events = 0
    total_inference_time = 0.0

    print("Edge inference service started with ONNX Runtime...")

    start = time.time()

    for message in consumer:
        event = message.value
        features = event_to_features(event)

        inference_start = time.time()
        prediction = session.run([output_name], {input_name: features})[0][0]
        total_inference_time += time.time() - inference_start

        total_events += 1

        if prediction == -1:
            forwarded_events += 1
        else:
            dropped_events += 1

        if total_events >= MAX_EVENTS_TO_PROCESS:
            break

    duration = time.time() - start
    reduction = (dropped_events / total_events) * 100
    avg_inference_ms = (total_inference_time / total_events) * 1000

    print("\n--- ONNX Edge Inference Summary ---")
    print(f"Total events processed: {total_events}")
    print(f"Forwarded anomaly events: {forwarded_events}")
    print(f"Dropped normal events: {dropped_events}")
    print(f"Cloud traffic reduction: {reduction:.2f}%")
    print(f"Average ONNX inference latency ms: {avg_inference_ms:.4f}")
    print(f"Duration seconds: {duration:.2f}")
    print(f"Processing throughput events/sec: {total_events / duration:.2f}")


if __name__ == "__main__":
    main()