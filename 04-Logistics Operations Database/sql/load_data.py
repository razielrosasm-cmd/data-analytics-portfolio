"""
load_data.py — Step 4: persist the three clean tables into SQLite.

Goal: make the clean CSVs queryable from SQLite so Step 5 (SQL analysis)
can be reproducible and auditable. The database is regenerated on every run
(drop + create + insert), so the same clean CSVs always produce the same .db.

Run with: py -3.12 sql/load_data.py
"""

import pandas as pd
import sqlite3
import os

# === CONFIG ===
PROJECT   = r"C:\Users\Anonymous\Desktop\projects\04-Logistics Operations Database"
PROCESSED = os.path.join(PROJECT, "data", "processed")
SQL_DIR   = os.path.join(PROJECT, "sql")
DB_DIR    = os.path.join(SQL_DIR, "db")
DB_PATH   = os.path.join(DB_DIR, "logistics.db")
SCHEMA    = os.path.join(SQL_DIR, "schema.sql")

os.makedirs(DB_DIR, exist_ok=True)

# Remove existing DB so the run is truly idempotent
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

TABLES = [
    ("master_driver_clean",      "master_driver_clean.csv"),
    ("master_trip_clean",        "master_trip_clean.csv"),
    ("master_truck_month_clean", "master_truck_month_clean.csv"),
]

# === LOAD ===
print("=" * 70)
print("LOADING CLEAN TABLES INTO SQLITE")
print("=" * 70)
print(f"Database: {DB_PATH}")
print()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Execute schema.sql — this drops any pre-existing tables and recreates them
with open(SCHEMA, "r", encoding="utf-8") as f:
    cursor.executescript(f.read())
print("Schema applied from schema.sql")
print()

for table_name, csv_name in TABLES:
    csv_path = os.path.join(PROCESSED, csv_name)
    df = pd.read_csv(csv_path)

    # Convert booleans to 0/1 (pandas writes True/False; SQLite prefers ints)
    for col in df.columns:
        if df[col].dtype == bool:
            df[col] = df[col].astype(int)

    df.to_sql(table_name, conn, if_exists="append", index=False)
    print(f"  {table_name:<30} <- {csv_name} ({len(df):,} rows)")

conn.commit()

# === VERIFY ===
print()
print("=" * 70)
print("VERIFICATION")
print("=" * 70)

for table_name, _ in TABLES:
    count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
    print(f"  {table_name:<30} {count:>10,} rows")

print()
print("Column preview (first row of each table):")
print()

for table_name, _ in TABLES:
    cols = [row[1] for row in cursor.execute(f"PRAGMA table_info({table_name})").fetchall()]
    first_row = cursor.execute(f"SELECT * FROM {table_name} LIMIT 1").fetchone()
    print(f"  [{table_name}]")
    for col, val in zip(cols, first_row):
        print(f"    {col:<30} = {val!r}")
    print()

# === PRAGMA table_info SNAPSHOT ===
print("=" * 70)
print("SCHEMA SNAPSHOT (PRAGMA table_info)")
print("=" * 70)

for table_name, _ in TABLES:
    print(f"\n[{table_name}]")
    info = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
    for cid, name, dtype, notnull, default, pk in info:
        pk_marker = " [PK]" if pk else ""
        print(f"  {name:<30} {dtype:<10}{pk_marker}")

conn.close()
print()
print("=" * 70)
print(f"Database ready: {DB_PATH}")
print("=" * 70)