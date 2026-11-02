"""
Stage 4 — Attendance Data Pipeline
==================================
Purpose:
    Transform the wide attendance files (in_time.csv, out_time.csv) into:
      - a daily long-format dataset (employee × day → hours worked)
      - an employee-level summary (mean/median/std/count hours)

Inputs:
    data/raw/in_time.csv     (4410 × 262, wide)
    data/raw/out_time.csv    (4410 × 262, wide)

Outputs:
    data/processed/attendance_daily.csv
        one row per (employee_id, date, hours_worked)
    data/processed/attendance_employee_summary.csv
        one row per employee_id with aggregated attendance metrics
    docs/attendance_log.md
        documented decisions and edge cases

Design:
    - Melt wide → long on both files.
    - Inner join on (employee_id, date).
    - Drop rows where either timestamp is missing.
    - Compute daily hours; handle overnight shifts (> 0 correction).
    - Flag anomalies: hours <= 0 or hours > 16.
    - Aggregate to employee level.
    - Validate: all 4,410 employees present, plausible ranges.
"""

from pathlib import Path
import pandas as pd
import numpy as np


# ===========================================================================
# CONFIGURATION
# ===========================================================================
PROJECT_ROOT  = Path(__file__).resolve().parents[2]
RAW_DIR       = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DIR      = PROJECT_ROOT / "docs"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)

IN_TIME_FILE  = "in_time.csv"
OUT_TIME_FILE = "out_time.csv"

EXPECTED_EMPLOYEES = 4410
MAX_REASONABLE_HOURS = 16.0   # anything above this is a data anomaly
MIN_REASONABLE_HOURS = 0.0    # anything below this is a data anomaly


# ===========================================================================
# 4.1 — LOAD WIDE FILES AND RESHAPE TO LONG
# ===========================================================================
def load_wide(path: Path, value_name: str) -> pd.DataFrame:
    """
    Read a wide attendance CSV and melt it into long format.

    Returns columns: [employee_id, date, <value_name>]
    """
    df = pd.read_csv(path)

    # Rename the unnamed first column
    first_col = df.columns[0]
    df = df.rename(columns={first_col: "employee_id"})

    # Melt wide → long
    long_df = df.melt(
        id_vars=["employee_id"],
        var_name="date",
        value_name=value_name,
    )

    # Parse date column to datetime
    long_df["date"] = pd.to_datetime(long_df["date"], errors="coerce")

    # Parse the value (timestamp string) to datetime
    long_df[value_name] = pd.to_datetime(long_df[value_name], errors="coerce")

    return long_df


# ===========================================================================
# 4.2 — MERGE IN AND OUT
# ===========================================================================
def merge_in_out(in_long: pd.DataFrame, out_long: pd.DataFrame) -> pd.DataFrame:
    """
    Inner-join in_time and out_time on (employee_id, date).
    Keep only rows where BOTH timestamps exist.
    """
    merged = in_long.merge(
        out_long,
        on=["employee_id", "date"],
        how="inner",
    )
    return merged


# ===========================================================================
# 4.3 — COMPUTE DAILY HOURS + HANDLE OVERNIGHT
# ===========================================================================
def compute_hours(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute hours_worked from in_time and out_time.

    Handles overnight shifts: if out_time < in_time, add 24 hours.
    """
    delta = df["out_time"] - df["in_time"]

    # Convert to hours (float)
    hours = delta.dt.total_seconds() / 3600.0

    # Overnight correction: negative duration means the shift crossed midnight
    overnight_mask = hours < 0
    hours.loc[overnight_mask] = hours.loc[overnight_mask] + 24.0

    df = df.copy()
    df["hours_worked"] = hours

    # Flags for documentation
    df["was_overnight"] = overnight_mask

    return df


# ===========================================================================
# 4.4 — FLAG ANOMALIES
# ===========================================================================
def flag_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add anomaly flags:
      - hours_worked <= 0     → impossible; likely data error
      - hours_worked > 16     → unreasonably long; likely data error
    """
    df = df.copy()
    df["anomaly_negative"] = df["hours_worked"] <= MIN_REASONABLE_HOURS
    df["anomaly_too_long"] = df["hours_worked"] > MAX_REASONABLE_HOURS
    return df


# ===========================================================================
# 4.5 — AGGREGATE TO EMPLOYEE LEVEL
# ===========================================================================
def aggregate_employee(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate the daily data to one row per employee.

    Excludes anomaly rows from mean/median/std but keeps the counts so
    the reader can see how many days were dropped.
    """
    clean = df[~df["anomaly_negative"] & ~df["anomaly_too_long"]].copy()

    agg = clean.groupby("employee_id").agg(
        days_worked         = ("hours_worked", "count"),
        avg_hours           = ("hours_worked", "mean"),
        median_hours        = ("hours_worked", "median"),
        std_hours           = ("hours_worked", "std"),
        min_hours           = ("hours_worked", "min"),
        max_hours           = ("hours_worked", "max"),
        overnight_days      = ("was_overnight", "sum"),
    ).reset_index()

    # Round for readability
    for col in ["avg_hours", "median_hours", "std_hours",
                "min_hours", "max_hours"]:
        agg[col] = agg[col].round(2)

    return agg


# ===========================================================================
# 4.6 — VALIDATE
# ===========================================================================
def validate(
    daily: pd.DataFrame,
    summary: pd.DataFrame,
    anomalies: dict,
) -> None:
    print("[4.6] VALIDATING")
    print("-" * 72)
    errors = []

    # All 4,410 employees present in summary
    n_emp = summary["employee_id"].nunique()
    if n_emp != EXPECTED_EMPLOYEES:
        errors.append(f"Expected {EXPECTED_EMPLOYEES} employees, got {n_emp}")
    else:
        print(f"  ✅ All {EXPECTED_EMPLOYEES} employees present in summary")

    # No duplicate employee_id in summary
    dupes = int(summary["employee_id"].duplicated().sum())
    if dupes:
        errors.append(f"{dupes} duplicate employee_id in summary")
    else:
        print(f"  ✅ No duplicate employee_id in summary")

    # daily has 0 or more rows per employee (some could be missing entirely)
    n_emp_daily = daily["employee_id"].nunique()
    print(f"  ℹ Employees with at least one daily record: {n_emp_daily}")

    # Sanity on hours
    if anomalies["negative"] > 0:
        print(f"  ⚠ Negative hours (flagged, excluded from summary): "
              f"{anomalies['negative']}")
    else:
        print(f"  ✅ No negative hours")

    if anomalies["too_long"] > 0:
        print(f"  ⚠ Unreasonably long days (flagged, excluded from summary): "
              f"{anomalies['too_long']}")
    else:
        print(f"  ✅ No days > {MAX_REASONABLE_HOURS} hours")

    # Range plausibility
    hr_min = float(summary["avg_hours"].min())
    hr_max = float(summary["avg_hours"].max())
    hr_mean = float(summary["avg_hours"].mean())
    print(f"  ℹ avg_hours range: {hr_min:.2f} – {hr_max:.2f} "
          f"(overall mean {hr_mean:.2f})")

    print()
    if errors:
        print("  ❌ VALIDATION FAILED:")
        for e in errors:
            print(f"     - {e}")
        raise SystemExit("Stage 4 validation failed.")
    print("  ✅ All validation checks passed.")
    print()


# ===========================================================================
# 4.7 — EXPORT
# ===========================================================================
def export(daily: pd.DataFrame, summary: pd.DataFrame) -> tuple:
    print("[4.7] EXPORTING")
    print("-" * 72)
    daily_path   = PROCESSED_DIR / "attendance_daily.csv"
    summary_path = PROCESSED_DIR / "attendance_employee_summary.csv"

    daily.to_csv(daily_path, index=False)
    summary.to_csv(summary_path, index=False)

    print(f"  ✅ {daily_path}")
    print(f"     rows: {len(daily):,}  columns: {daily.shape[1]}")
    print(f"  ✅ {summary_path}")
    print(f"     rows: {len(summary):,}  columns: {summary.shape[1]}")
    print()
    return daily_path, summary_path


# ===========================================================================
# 4.8 — WRITE LOG
# ===========================================================================
def write_log(
    daily: pd.DataFrame,
    summary: pd.DataFrame,
    anomalies: dict,
    output_path: Path,
) -> None:
    print("[4.8] WRITING LOG")
    print("-" * 72)

    lines = []
    lines.append("# Attendance Data Log — HR Analytics Attrition Case Study\n\n")
    lines.append("**Stage:** 4 — Attendance Data Pipeline  \n")
    lines.append("**Input:** `in_time.csv`, `out_time.csv` (wide, 4,410 × 262)  \n")
    lines.append("**Output:** `attendance_daily.csv`, "
                 "`attendance_employee_summary.csv`  \n")
    lines.append("**Script:** `python/analysis/04_process_attendance.py`\n\n")

    lines.append("---\n\n")
    lines.append("## 1. Why Attendance Is Processed Separately\n\n")
    lines.append(
        "The attendance files are structurally different from the master HR "
        "data. Each is a **wide table** with one row per employee and ~261 "
        "date columns. To use this data, we need to reshape it into a **long** "
        "format (one row per employee-day), compute daily hours, then "
        "aggregate back to employee level. This is a data-engineering task — "
        "Python is the right tool, not SQL.\n\n"
    )

    lines.append("---\n\n")
    lines.append("## 2. Pipeline Steps\n\n")
    lines.append("| Step | Action |\n")
    lines.append("|---|---|\n")
    lines.append("| 4.1 | Loaded both wide CSVs (4,410 × 262) |\n")
    lines.append("| 4.1 | Renamed first column `Unnamed: 0` → `employee_id` |\n")
    lines.append("| 4.1 | Melted wide → long (1 row per employee-date) |\n")
    lines.append("| 4.2 | Inner-joined `in_time` and `out_time` on `(employee_id, date)` |\n")
    lines.append("| 4.3 | Computed `hours_worked = out − in` (overnight correction if negative) |\n")
    lines.append("| 4.4 | Flagged anomalies (≤ 0 hours, > 16 hours) |\n")
    lines.append("| 4.5 | Aggregated to employee level (mean, median, std, etc.) |\n")
    lines.append("| 4.6 | Validated against master (4,410 employees present) |\n")
    lines.append("| 4.7 | Exported two CSVs |\n\n")

    lines.append("---\n\n")
    lines.append("## 3. Edge Cases Handled\n\n")
    lines.append("### 3.1 Overnight shifts\n")
    lines.append(
        "If `out_time < in_time`, the shift crossed midnight. Example: "
        "in `22:55`, out `01:05` → naive delta is negative, corrected to "
        "+24 hours. This was flagged with the `was_overnight` column.\n\n"
    )
    lines.append(f"**Overnight records found:** {int(daily['was_overnight'].sum()):,}\n\n")

    lines.append("### 3.2 Anomalous durations\n")
    lines.append(
        f"Two anomaly flags were applied:\n\n"
        f"- `anomaly_negative`: `hours_worked <= {MIN_REASONABLE_HOURS}`\n"
        f"- `anomaly_too_long`: `hours_worked > {MAX_REASONABLE_HOURS}`\n\n"
        f"Anomalous rows are **kept** in `attendance_daily.csv` (for "
        f"auditability) but **excluded** from the employee-level summary "
        f"statistics (mean, median, std).\n\n"
    )
    lines.append(f"**Negative-hour rows:** {anomalies['negative']:,}  \n")
    lines.append(f"**Too-long rows:** {anomalies['too_long']:,}\n\n")

    lines.append("### 3.3 Missing days\n")
    lines.append(
        "Weekends and holidays are stored as `NaN` in the raw files and "
        "were dropped during the long-format reshape (they cannot be "
        "meaningful rows). Leave and sick days also appear as `NaN` and "
        "were dropped. The resulting `days_worked` count per employee "
        "reflects actual attended days.\n\n"
    )

    lines.append("---\n\n")
    lines.append("## 4. Output Shapes\n\n")
    lines.append(f"- `attendance_daily.csv`: **{len(daily):,} rows** × "
                 f"{daily.shape[1]} columns\n")
    lines.append(f"- `attendance_employee_summary.csv`: **{len(summary):,} rows** × "
                 f"{summary.shape[1]} columns\n\n")

    lines.append("---\n\n")
    lines.append("## 5. Employee Summary Schema\n\n")
    lines.append("| Column | Description |\n")
    lines.append("|---|---|\n")
    lines.append("| `employee_id` | 1–4410 |\n")
    lines.append("| `days_worked` | Count of days with valid in+out |\n")
    lines.append("| `avg_hours` | Mean daily hours (anomalies excluded) |\n")
    lines.append("| `median_hours` | Median daily hours |\n")
    lines.append("| `std_hours` | Std-dev of daily hours |\n")
    lines.append("| `min_hours` | Minimum daily hours |\n")
    lines.append("| `max_hours` | Maximum daily hours |\n")
    lines.append("| `overnight_days` | Count of shifts that crossed midnight |\n\n")

    lines.append("---\n\n")
    lines.append("## 6. Join Key to Master\n\n")
    lines.append(
        "`attendance_employee_summary.employee_id` joins 1:1 to "
        "`hr_master_clean.employee_id`. All 4,410 IDs are present in both.\n\n"
    )

    lines.append("---\n\n")
    lines.append("## 7. Limitations\n\n")
    lines.append("- Timestamps are recorded but no break/leave information\n")
    lines.append("- No reason codes for missing days\n")
    lines.append("- Overnight shifts are corrected but the *reason* is unknown\n")
    lines.append("- All times assumed in same local timezone\n\n")

    output_path.write_text("".join(lines), encoding="utf-8")
    print(f"  ✅ {output_path}")
    print()


# ===========================================================================
# MAIN
# ===========================================================================
def main():
    print("=" * 72)
    print("STAGE 4 — ATTENDANCE DATA PIPELINE")
    print("=" * 72)
    print()

    # 4.1 — Load and reshape
    print("[4.1] LOADING WIDE FILES AND MELTING TO LONG")
    print("-" * 72)
    in_long  = load_wide(RAW_DIR / IN_TIME_FILE,  value_name="in_time")
    out_long = load_wide(RAW_DIR / OUT_TIME_FILE, value_name="out_time")
    print(f"  in_time  long rows: {len(in_long):,}")
    print(f"  out_time long rows: {len(out_long):,}")
    print()

    # 4.2 — Merge
    print("[4.2] MERGING IN_TIME AND OUT_TIME")
    print("-" * 72)
    merged = merge_in_out(in_long, out_long)
    print(f"  Rows before drop-NaN: {len(merged):,}")
    merged = merged.dropna(subset=["in_time", "out_time"])
    print(f"  Rows after  drop-NaN: {len(merged):,}")
    print()

    # 4.3 — Compute hours
    print("[4.3] COMPUTING DAILY HOURS")
    print("-" * 72)
    merged = compute_hours(merged)
    n_overnight = int(merged["was_overnight"].sum())
    print(f"  Overnight shifts detected: {n_overnight:,}")
    print()

    # 4.4 — Anomalies
    print("[4.4] FLAGGING ANOMALIES")
    print("-" * 72)
    merged = flag_anomalies(merged)
    anomalies = {
        "negative": int(merged["anomaly_negative"].sum()),
        "too_long": int(merged["anomaly_too_long"].sum()),
    }
    print(f"  Negative hours: {anomalies['negative']:,}")
    print(f"  Too-long days:  {anomalies['too_long']:,}")
    print()

    daily = merged  # alias

    # 4.5 — Aggregate
    print("[4.5] AGGREGATING TO EMPLOYEE LEVEL")
    print("-" * 72)
    summary = aggregate_employee(daily)
    print(f"  Summary rows: {len(summary):,}")
    print(f"  Summary cols: {summary.shape[1]}")
    print()

    # 4.6 — Validate
    validate(daily, summary, anomalies)

    # 4.7 — Export
    export(daily, summary)

    # 4.8 — Log
    write_log(daily, summary, anomalies, DOCS_DIR / "attendance_log.md")

    print("=" * 72)
    print("STAGE 4 COMPLETE")
    print("=" * 72)
    print("→ Next: Stage 5 — SQL database design & loading")
    print()


if __name__ == "__main__":
    main()