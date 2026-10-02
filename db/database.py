import sqlite3
import json
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fraudshield.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        amount REAL, hour REAL, merchant_risk REAL,
        distance_from_home REAL, transaction_velocity REAL,
        is_international REAL,
        discriminant_score REAL,
        discriminant_verdict TEXT,
        discriminant_details TEXT,
        svm_score REAL,
        svm_verdict TEXT,
        svm_details TEXT,
        is_fraud_predicted INTEGER
    )''')
    conn.commit()
    conn.close()

def save_transaction(features: dict, disc_result: dict, svm_result: dict, is_fraud: bool) -> int:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''INSERT INTO transactions 
        (timestamp, amount, hour, merchant_risk, distance_from_home,
         transaction_velocity, is_international,
         discriminant_score, discriminant_verdict, discriminant_details,
         svm_score, svm_verdict, svm_details, is_fraud_predicted)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (datetime.now().isoformat(),
         features.get('amount'), features.get('hour'),
         features.get('merchant_risk'), features.get('distance_from_home'),
         features.get('transaction_velocity'), features.get('is_international'),
         disc_result.get('raw_score'), disc_result.get('verdict'),
         json.dumps(disc_result),
         svm_result.get('decision_value'), svm_result.get('verdict'),
         json.dumps(svm_result),
         int(is_fraud)))
    conn.commit()
    txn_id = cur.lastrowid
    conn.close()
    return txn_id

def get_history(limit: int = 50) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]
