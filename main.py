import time
from generator import generate_transaction
from validator import DataQualityValidator
from lakehouse_writer import MockIcebergLakehouse

def run_pipeline(num_cycles=10):
    print("🚀 Starting Integrated IceStream Lakehouse Pipeline...")
    validator = DataQualityValidator(error_threshold_percent=20.0)
    lakehouse = MockIcebergLakehouse()
    
    for i in range(num_cycles):
        print(f"\n--- Processing Cycle {i+1} ---")
        txn = generate_transaction()
        print(f"Generated: {txn['transaction_id']}")
        
        # Check for data quality anomalies
        anomalies = []
        if "tax_amount" not in txn or txn["tax_amount"] is None:
            anomalies.append("NULL_TAX")
        if "payment_method" not in txn:
            anomalies.append("MISSING_PAYMENT_METHOD")
            
        # Determine if it goes to DLQ or Main Table
        is_dlq = len(anomalies) > 0
        if is_dlq:
            print(f"🚨 Anomaly flagged: {anomalies} -> Routing to DLQ")
            validator.anomaly_count += 1
        else:
            print("[PASS] Validation passed -> Writing to Main Table")
            
        validator.total_records += 1
        
        # Write record to Lakehouse storage
        lakehouse.append_record(txn, is_dlq=is_dlq)
        
        time.sleep(0.5)

    print("\n✅ Pipeline batch run completed successfully!")

if __name__ == "__main__":
    run_pipeline(num_cycles=5)