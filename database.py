import sqlite3
import pandas as pd

DB_NAME = "receipts.db"

async def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS receipts (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            photo_id TEXT,
            amount TEXT,
            comment TEXT,
            company TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_receipt(user_id, photo_id, amount, comment, company):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO receipts (user_id, photo_id, amount, comment, company)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, photo_id, amount, comment, company))
    conn.commit()
    conn.close()

def export_to_excel(company=None):
    conn = sqlite3.connect(DB_NAME)
    if company:
        df = pd.read_sql_query("SELECT * FROM receipts WHERE company = ?", conn, params=(company,))
    else:
        df = pd.read_sql_query("SELECT * FROM receipts", conn)
    path = f"export_{company or 'all'}.xlsx"
    df.to_excel(path, index=False)
    conn.close()
    return path
