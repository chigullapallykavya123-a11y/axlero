import streamlit as st
import time
import random

st.set_page_config(page_title="IceStream - Lakehouse Observability", layout="wide")

st.title("🧊 IceStream: Real-Time Lakehouse Observability")
st.markdown("### Pipeline Health & Circuit Breaker Dashboard")

# Top metrics row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ingestion Rate", "1,245 tx/sec", "+12%")
col2.metric("Active Anomalies", "3 detected", "-2%")
col3.metric("Circuit Breaker Status", "TRIPPED (DLQ Active)", "⚠️")
col4.metric("Iceberg Catalog Latency", "45 ms", "-5ms")

st.markdown("---")

# Pipeline Flow Visualization Section
st.subheader("🔄 Data Pipeline Lineage & Node Status")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("### 1. Ingestion")
    st.info("Kafka Stream\nStatus: **Healthy**")

with c2:
    st.markdown("### 2. Processing")
    st.info("Apache Flink\nStatus: **Active**")

with c3:
    st.markdown("### 3. Validation")
    st.error("Great Expectations\nStatus: **Circuit Breaker Tripped**")

with c4:
    st.markdown("### 4. Storage / DLQ")
    st.warning("Apache Iceberg / DLQ\nStatus: **Quarantining Bad Data**")

st.markdown("---")

# Incident Log Section
st.subheader("🚨 Live Incident Log & Quarantine Queue")

incident_data = [
    {"Time": "13:21:40", "Node": "Validation", "Error": "NULL_OR_MISSING_TAX_AMOUNT", "Action": "Routed to DLQ"},
    {"Time": "13:21:42", "Node": "Validation", "Error": "SCHEMA_DRIFT_MISSING_PAYMENT_METHOD", "Action": "Quarantined"},
    {"Time": "13:21:45", "Node": "Circuit Breaker", "Error": "Error rate exceeded 5.0%", "Action": "Pipeline Paused Red"}
]

st.table(incident_data)

if st.button("🔄 Refresh Pipeline Status"):
    st.rerun()