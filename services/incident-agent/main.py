import time
import psycopg2


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
        SELECT device_id, temperature, pressure, vibration, voltage,
               current_value, rpm, humidity, severity, created_at
        FROM anomaly_events
        ORDER BY id DESC
        LIMIT 1;
        """
    )

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    return row


def generate_root_cause(event):
    (
        device_id,
        temperature,
        pressure,
        vibration,
        voltage,
        current_value,
        rpm,
        humidity,
        severity,
        created_at,
    ) = event

    causes = []
    recommendations = []

    if vibration > 1.0 and rpm > 2200:
        causes.append("bearing wear, rotor imbalance, or shaft misalignment")
        recommendations.append("inspect bearings, validate shaft alignment, and schedule vibration analysis")

    if temperature > 90 and current_value > 15:
        causes.append("motor overload, cooling failure, or lubrication breakdown")
        recommendations.append("inspect cooling system, check lubricant levels, and reduce machine load")

    if voltage < 205 and current_value > 15:
        causes.append("power supply instability or motor winding stress")
        recommendations.append("inspect power supply, wiring, and motor windings")

    if pressure > 50 and temperature > 90:
        causes.append("pump blockage, valve restriction, or fluid flow obstruction")
        recommendations.append("inspect valves, filters, and downstream pressure points")

    if humidity > 65:
        causes.append("moisture exposure or enclosure sealing issue")
        recommendations.append("inspect seals and verify enclosure protection")

    if not causes:
        causes.append("general equipment degradation pattern")
        recommendations.append("schedule preventive inspection and continue monitoring")

    return {
        "device_id": device_id,
        "severity": severity,
        "root_cause": "; ".join(causes),
        "recommendation": "; ".join(recommendations),
        "generated_at": str(created_at),
    }


def main():
    start = time.time()

    latest_event = get_latest_anomaly()

    if not latest_event:
        print("No anomaly events found.")
        return

    report = generate_root_cause(latest_event)

    duration = time.time() - start

    print("\n--- Incident Analysis Report ---")
    print(f"Device ID: {report['device_id']}")
    print(f"Severity: {report['severity']}")
    print(f"Root Cause: {report['root_cause']}")
    print(f"Recommendation: {report['recommendation']}")
    print(f"Response time seconds: {duration:.4f}")


if __name__ == "__main__":
    main()