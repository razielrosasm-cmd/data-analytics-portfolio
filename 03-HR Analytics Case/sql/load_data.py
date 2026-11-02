"""
Stage 5 — SQL Database Loader
HR Analytics Attrition Case Study

Creates sql/hr_attrition.db from:
  - data/processed/hr_master_clean.csv
  - data/processed/attendance_employee_summary.csv

Also populates 8 dimension tables with hardcoded code->label lookups.
"""

import sqlite3
from pathlib import Path
import pandas as pd

# ---------- PATHS ----------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH      = PROJECT_ROOT / "sql" / "hr_attrition.db"
SCHEMA_PATH  = PROJECT_ROOT / "sql" / "schema.sql"
MASTER_CSV   = PROJECT_ROOT / "data" / "processed" / "hr_master_clean.csv"
ATTEND_CSV   = PROJECT_ROOT / "data" / "processed" / "attendance_employee_summary.csv"


# ---------- DIMENSION LOOKUPS ----------
DIMENSIONS = {
    "dim_education": (
        ["education_code", "education_label"],
        [
            (1, "Below College"),
            (2, "College"),
            (3, "Bachelor"),
            (4, "Master"),
            (5, "Doctor"),
        ],
    ),
    "dim_environment_satisfaction": (
        ["env_sat_code", "env_sat_label"],
        [
            (1, "Low"),
            (2, "Medium"),
            (3, "High"),
            (4, "Very High"),
        ],
    ),
    "dim_job_involvement": (
        ["job_involvement_code", "job_involvement_label"],
        [
            (1, "Low"),
            (2, "Medium"),
            (3, "High"),
            (4, "Very High"),
        ],
    ),
    "dim_job_level": (
        ["job_level_code", "job_level_label"],
        [
            (1, "Entry"),
            (2, "Junior"),
            (3, "Mid"),
            (4, "Senior"),
            (5, "Executive"),
        ],
    ),
    "dim_job_satisfaction": (
        ["job_sat_code", "job_sat_label"],
        [
            (1, "Low"),
            (2, "Medium"),
            (3, "High"),
            (4, "Very High"),
        ],
    ),
    "dim_performance_rating": (
        ["perf_rating_code", "perf_rating_label"],
        [
            (1, "Low"),
            (2, "Good"),
            (3, "Excellent"),
            (4, "Outstanding"),
        ],
    ),
    "dim_stock_option_level": (
        ["stock_option_code", "stock_option_label"],
        [
            (0, "None"),
            (1, "Low"),
            (2, "Medium"),
            (3, "High"),
        ],
    ),
    "dim_work_life_balance": (
        ["wlb_code", "wlb_label"],
        [
            (1, "Bad"),
            (2, "Good"),
            (3, "Better"),
            (4, "Best"),
        ],
    ),
}


def build_database() -> None:
    # Delete any existing DB so we always start fresh (idempotent rebuild).
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"[reset] removed existing {DB_PATH.name}")

    # Read schema and create tables.
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(schema_sql)
    print(f"[schema] created tables from {SCHEMA_PATH.name}")

    # ---------- LOAD DIMENSIONS ----------
    for table, (cols, rows) in DIMENSIONS.items():
        placeholders = ", ".join(["?"] * len(cols))
        col_list     = ", ".join(cols)
        conn.executemany(
            f"INSERT INTO {table} ({col_list}) VALUES ({placeholders})",
            rows,
        )
        print(f"[dim]   {table:<35} {len(rows)} rows")

    # ---------- LOAD FACT: EMPLOYEE ----------
    df_master = pd.read_csv(MASTER_CSV)
    df_master.to_sql("fact_employee", conn, if_exists="append", index=False)
    print(f"[fact]  fact_employee{'':<22} {len(df_master)} rows")

    # ---------- LOAD FACT: ATTENDANCE SUMMARY ----------
    df_attend = pd.read_csv(ATTEND_CSV)
    df_attend.to_sql("attendance_summary", conn, if_exists="append", index=False)
    print(f"[fact]  attendance_summary{'':<15} {len(df_attend)} rows")

    conn.commit()
    conn.close()
    print(f"\n[done]  database written to {DB_PATH}")


if __name__ == "__main__":
    build_database()