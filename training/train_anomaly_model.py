import os
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType


MODEL_DIR = "models"
ONNX_MODEL_PATH = os.path.join(MODEL_DIR, "anomaly_detector.onnx")
SKLEARN_MODEL_PATH = os.path.join(MODEL_DIR, "anomaly_detector.joblib")


def generate_training_data(rows: int = 50000):
    normal_data = np.column_stack([
        np.random.uniform(65, 85, rows),
        np.random.uniform(30, 45, rows),
        np.random.uniform(0.1, 0.6, rows),
        np.random.uniform(210, 240, rows),
        np.random.uniform(5, 12, rows),
        np.random.uniform(1200, 1800, rows),
        np.random.uniform(30, 55, rows),
    ])

    return normal_data.astype(np.float32)


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)

    x_train = generate_training_data()

    model = IsolationForest(
        n_estimators=100,
        contamination=0.15,
        random_state=42,
    )

    model.fit(x_train)

    joblib.dump(model, SKLEARN_MODEL_PATH)

    initial_type = [("float_input", FloatTensorType([None, 7]))]
    onnx_model = convert_sklearn(
        model,
        initial_types=initial_type,
        target_opset={"": 17, "ai.onnx.ml": 3},
    )

    with open(ONNX_MODEL_PATH, "wb") as f:
        f.write(onnx_model.SerializeToString())

    print("--- Model Training Summary ---")
    print(f"Training rows: {len(x_train)}")
    print(f"Features: 7")
    print(f"Saved sklearn model: {SKLEARN_MODEL_PATH}")
    print(f"Saved ONNX model: {ONNX_MODEL_PATH}")


if __name__ == "__main__":
    main()