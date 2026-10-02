import csv
import io
from typing import BinaryIO

FEATURE_NAMES = ['amount', 'hour', 'merchant_risk', 'distance_from_home', 'transaction_velocity', 'is_international']

def parse_csv(file_content: bytes) -> list[dict]:
    """Parse a CSV file containing transactions.
    Expects columns matching FEATURE_NAMES (order doesn't matter, matched by header).
    Returns list of dicts with float values.
    """
    text = file_content.decode('utf-8-sig')  # handle BOM
    reader = csv.DictReader(io.StringIO(text))
    transactions = []
    for row in reader:
        txn = {}
        for name in FEATURE_NAMES:
            if name in row:
                txn[name] = float(row[name])
            else:
                raise ValueError(f"Missing column: {name}")
        transactions.append(txn)
    return transactions
