import time
import psycopg2

from services.incident_agent.langgraph_agent import incident_agent


DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "predictive_maintenance",
    "user": "edgeai",
    "password": "edgeai",
}


def get_latest_anomaly():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT device_id, event_timestamp, temperature, pressure, vibration,
               voltage, current_value, rpm, humidity, anomaly_score, severity
        FROM anomaly_events
        ORDER BY id DESC
        LIMIT 1;
        """
    )

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return None

    return {
        "device_id": row[0],
        "timestamp": str(row[1]),
        "temperature": row[2],
        "pressure": row[3],
        "vibration": row[4],
        "voltage": row[5],
        "current": row[6],
        "rpm": row[7],
        "humidity": row[8],
        "anomaly_score": row[9],
        "severity": row[10],
    }


def main():
    anomaly = get_latest_anomaly()

    if not anomaly:
        print("No anomaly found.")
        return

    start = time.time()

    result = incident_agent.invoke(
        {
            "anomaly": anomaly,
            "context": [],
            "report": "",
        }
    )

    duration = time.time() - start

    print("\n--- LangGraph Incident Analysis Report ---")
    print(result["report"])
    print(f"\nResponse time seconds: {duration:.4f}")


if __name__ == "__main__":
    main()