# Edge AI Predictive Maintenance Platform

> **Distributed Edge AI platform for real-time predictive maintenance using FastAPI, Kafka, Redis, PostgreSQL, ONNX Runtime, and agentic incident analysis.**

## Overview

This project simulates an industrial IoT environment where thousands of edge devices continuously stream telemetry data. Instead of forwarding every sensor reading to the cloud, anomaly detection is performed directly at the edge using an ONNX Runtime model. Only anomalous events are transmitted to the cloud, significantly reducing bandwidth usage while enabling real-time predictive maintenance.

The cloud platform stores anomaly events in PostgreSQL, caches recent device state in Redis, and generates explainable maintenance recommendations through an incident analysis workflow.

---

# Architecture

```text
                 +---------------------------+
                 |   Telemetry Simulator     |
                 | 5000 Simulated Devices    |
                 +-------------+-------------+
                               |
                               |
                               v
                     +------------------+
                     |      Kafka       |
                     | telemetry-events |
                     +--------+---------+
                              |
                              |
                              v
                +-----------------------------+
                | Edge Inference Service      |
                | ONNX Runtime                |
                | Isolation Forest            |
                +-------------+---------------+
                              |
                 Normal        |        Anomaly
                 Drop          |        Forward
                              v
                  +---------------------------+
                  | FastAPI Cloud API         |
                  +------------+--------------+
                               |
                     +---------+---------+
                     |                   |
                     v                   v
              PostgreSQL             Redis Cache
                     |
                     v
         Incident Analysis Workflow
                     |
                     v
      Root Cause + Maintenance Recommendation
```

---

# Features

* Simulates telemetry from 5,000 industrial IoT devices
* Streams telemetry through Apache Kafka
* Performs edge-side anomaly detection using ONNX Runtime
* Filters normal events before cloud transmission
* Stores anomaly events in PostgreSQL
* Caches latest device state in Redis
* REST API built with FastAPI
* Generates explainable incident reports
* Dockerized infrastructure
* Modular microservice architecture

---

# Technology Stack

| Layer      | Technology       |
| ---------- | ---------------- |
| Language   | Python           |
| API        | FastAPI          |
| Messaging  | Apache Kafka     |
| Database   | PostgreSQL       |
| Cache      | Redis            |
| ML         | Isolation Forest |
| Inference  | ONNX Runtime     |
| Containers | Docker Compose   |

---

# Project Structure

```text
Edge-AI-Predictive-Maintenance-Platform/

├── services/
│   ├── telemetry-simulator/
│   ├── edge-inference/
│   ├── cloud-api/
│   └── incident-agent/
│
├── training/
│
├── models/
│
├── database/
│
├── docs/
│
├── screenshots/
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# System Workflow

1. Simulated IoT devices generate telemetry.
2. Telemetry is published to Kafka.
3. Edge inference consumes telemetry.
4. ONNX Runtime performs anomaly detection.
5. Normal events are discarded.
6. Only anomalies are sent to the FastAPI Cloud API.
7. Cloud API stores anomalies in PostgreSQL.
8. Latest anomaly is cached in Redis.
9. Incident Analysis generates maintenance recommendations.

---

# Running the Project

## Start Infrastructure

```bash
docker compose up -d
```

---

## Create Kafka Topic

```bash
docker exec -it edgeai-kafka kafka-topics \
  --create \
  --topic telemetry-events \
  --bootstrap-server localhost:9092 \
  --partitions 3 \
  --replication-factor 1
```

---

## Train the ONNX Model

```bash
python training/train_anomaly_model.py
```

---

## Start Cloud API

```bash
cd services/cloud-api
uvicorn main:app --reload --port 8000
```

---

## Generate Telemetry

```bash
python services/telemetry-simulator/main.py
```

---

## Run Edge Inference

```bash
python services/edge-inference/main.py
```

---

## Generate Incident Analysis

```bash
python services/incident-agent/main.py
```

---

# API Endpoints

## Health Check

```
GET /health
```

Returns

```json
{
    "status":"healthy"
}
```

---

## Store Anomaly

```
POST /anomalies
```

Stores anomaly information in PostgreSQL and Redis.

---

# Benchmark Results

| Metric                       | Result        |
| ---------------------------- | ------------- |
| Simulated Devices            | 5,000         |
| Telemetry Events (benchmark) | 10,000+       |
| PostgreSQL Stored Events     | 2,700+        |
| Cloud Traffic Reduction      | ~85%          |
| Edge Inference               | ONNX Runtime  |
| Incident Analysis            | Sub-3 seconds |

---

# Future Improvements

* Kubernetes deployment
* Prometheus metrics
* Grafana dashboards
* Real-time WebSocket monitoring
* Azure OpenAI powered incident reasoning
* Vector database integration
* Multi-edge deployment
* Distributed Kafka cluster

---

# License

MIT License
