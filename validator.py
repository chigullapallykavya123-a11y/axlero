import json
import time
from datetime import datetime

class DataQualityValidator:
    def __init__(self, error_threshold_percent=2.0):
        self.total_records = 0
        self.anomaly_count = 0
        self.error_threshold = error_threshold_percent

    def validate_record(self, record: dict):
        """Applies data quality assertions to a single transaction record."""
        self.total_records += 1
        anomalies = []

        # Rule 1: Check for missing or null tax amount (expect_column_values_to_not_be_null)
        if "tax_amount" not in record or record["tax_amount"] is None:
            anomalies.append("NULL_OR_MISSING_TAX_AMOUNT")

        # Rule 2: Check for schema drift (missing expected 'payment_method')
        if "payment_method" not in record:
            anomalies.append("SCHEMA_DRIFT_MISSING_PAYMENT_METHOD")

        # Rule 3: Check for unexpected legacy fields
        if "legacy_flag" in record:
            anomalies.append("SCHEMA_DRIFT_UNEXPECTED_LEGACY_FLAG")

        if anomalies:
            self.anomaly_count += 1
            self.handle_anomaly(record, anomalies)
        else:
            print(f"[PASS] Record {record.get('transaction_id')} passed validation.")

        self.check_circuit_breaker()

    def handle_anomaly(self, record, anomalies):
        """Quarantines bad data and logs the anomaly."""
        print(f"🚨 [FAIL] Anomaly detected in {record.get('transaction_id')}: {anomalies}")

    def check_circuit_breaker(self):
        """Circuit Breaker Logic: If error rate exceeds threshold, trip the breaker."""
        if self.total_records > 0:
            error_rate = (self.anomaly_count / self.total_records) * 100
            if error_rate > self.error_threshold:
                print(f"🔥 CIRCUIT BREAKER TRIPPED! Error rate at {error_rate:.2f}% exceeds threshold ({self.error_threshold}%). Routing stream to Dead Letter Queue (DLQ)...")

if __name__ == "__main__":
    validator = DataQualityValidator(error_threshold_percent=5.0)
    
    print("Starting Observability Validation Engine...\n")
    
    # Simulate processing a few sample transactions (some clean, some anomalous)
    sample_stream = [
        {"transaction_id": "txn_101", "tax_amount": 12.50, "payment_method": "Credit Card"},
        {"transaction_id": "txn_102", "tax_amount": None, "payment_method": "PayPal"},  # Null tax anomaly
        {"transaction_id": "txn_103", "tax_amount": 5.00, "legacy_flag": True},       # Schema drift anomaly
        {"transaction_id": "txn_104", "tax_amount": 8.20, "payment_method": "Debit Card"},
    ]

    for txn in sample_stream:
        validator.validate_record(txn)
        time.sleep(0.5)