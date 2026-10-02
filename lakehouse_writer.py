import json
import os
from datetime import datetime

class MockIcebergLakehouse:
    def __init__(self, storage_path="lakehouse_storage.json"):
        self.storage_path = storage_path
        # Initialize storage file if it doesn't exist
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w") as f:
                json.dump([], f)

    def append_record(self, record: dict, is_dlq: bool = False):
        """Appends a record to the appropriate Iceberg table (Main or Dead Letter Queue)."""
        target_table = "DLQ_Table" if is_dlq else "Main_Transactions_Table"
        
        # Add lakehouse metadata/snapshot timestamp
        lakehouse_record = {
            "snapshot_id": f"snap_{int(datetime.utcnow().timestamp())}",
            "table": target_table,
            "data": record
        }

        # Read existing data, append new record, and write back (Simulating ACID write)
        try:
            with open(self.storage_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []

        data.append(lakehouse_record)

        with open(self.storage_path, "w") as f:
            json.dump(data, f, indent=4)
            
        print(f"[ICELAKE] Appended transaction to [{target_table}] with snapshot ID.")

    def time_travel_query(self, snapshot_id):
        """Simulates an Iceberg time-travel query to read state at a specific snapshot."""
        print(f"\n[TIME TRAVEL] Querying lakehouse state for snapshot: {snapshot_id}")
        with open(self.storage_path, "r") as f:
            data = json.load(f)
            
        results = [item for item in data if item["snapshot_id"] == snapshot_id]
        print(f"Found {len(results)} record(s) in snapshot {snapshot_id}.")
        return results

if __name__ == "__main__":
    lakehouse = MockIcebergLakehouse()
    
    print("Testing Lakehouse Storage & ACID Append...\n")
    
    # Simulate writing clean data to Main Table and bad data to DLQ
    sample_clean_txn = {"transaction_id": "txn_201", "tax_amount": 15.00, "payment_method": "Credit Card"}
    sample_bad_txn = {"transaction_id": "txn_202", "tax_amount": None, "payment_method": "PayPal"}

    lakehouse.append_record(sample_clean_txn, is_dlq=False)
    lakehouse.append_record(sample_bad_txn, is_dlq=True)
    
    # Test time travel query simulation
    lakehouse.time_travel_query("snap_")