import json
import random
import time
from datetime import datetime

# Mock e-commerce categories and locations
CATEGORIES = ["Electronics", "Apparel", "Home & Kitchen", "Books", "Sports"]
PAYMENT_METHODS = ["Credit Card", "PayPal", "Apple Pay", "Debit Card"]

def generate_transaction():
    """Generates a mock e-commerce checkout transaction with occasional anomalies."""
    
    # Intentionally inject null values occasionally to test observability rules
    is_null_tax = random.random() < 0.05  # 5% chance of null tax amount
    is_schema_drift = random.random() < 0.02  # 2% chance of schema change/missing field
    
    transaction = {
        "transaction_id": f"txn_{random.randint(100000, 999999)}",
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": f"user_{random.randint(1000, 5000)}",
        "category": random.choice(CATEGORIES),
        "quantity": random.randint(1, 5),
        "unit_price": round(random.uniform(10.0, 500.0), 2),
        "tax_amount": None if is_null_tax else round(random.uniform(1.0, 50.0), 2),
        "payment_method": random.choice(PAYMENT_METHODS),
    }

    # Simulate schema drift by dropping a standard field randomly
    if is_schema_drift:
        transaction.pop("payment_method", None)
        transaction["legacy_flag"] = True # Unexpected new field

    return transaction

if __name__ == "__main__":
    print("Starting E-commerce Transaction Stream Generator...")
    print("Press Ctrl+C to stop.\n")
    
    try:
        while True:
            txn = generate_transaction()
            print(json.dumps(txn))
            # Simulate high-velocity streaming (e.g., transactions per second)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nStream generator stopped.")