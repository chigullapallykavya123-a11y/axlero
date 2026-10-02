# 🧊 IceStream: Real-Time Lakehouse Observability

An enterprise-grade, real-time data lakehouse observability and automated data quality pipeline built to prevent downstream pipeline failures.

## 🚀 Architecture & Features
* **Streaming Ingestion Engine (`generator.py`):** Generates high-velocity mock e-commerce transactions with intentional anomalies (null values and schema drift).
* **Observability Rules Engine (`validator.py`):** Applies Great Expectations-style validation assertions and circuit breaker logic to quarantine bad data when error rates exceed thresholds.
* **ACID Lakehouse Storage (`lakehouse_writer.py`):** Simulates Apache Iceberg table management, supporting snapshot isolation and time-travel queries.
* **Interactive UI Dashboard (`dashboard.py`):** A Streamlit-based operational UI displaying pipeline lineage nodes, status indicators, and live incident logs.

## 🛠️ How to Run
1. Run the integrated pipeline batch:
   ```bash
   python main.py