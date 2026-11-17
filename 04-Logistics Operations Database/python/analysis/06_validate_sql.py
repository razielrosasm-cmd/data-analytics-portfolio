"""
06_validate_sql.py — Step 6: SQL <-> Python cross-check.

Goal: re-run the four headline SQL findings in pandas and confirm exact
      agreement. If SQL != Python on any check, the pipeline stops — the
      executive summary would be wrong otherwise.

Run with: py -3.12 python/analysis/06_validate_sql.py

Exit codes:
    0  — all four checks passed
    1  — at least one check failed (stop and investigate)
"""

import pandas as pd
import os
import sys

# === CONFIG ===
PROJECT   = r"C:\Users\Anonymous\Desktop\projects\04-Logistics Operations Database"
PROCESSED = os.path.join(PROJECT, "data", "processed")
OUTPUTS   = os.path.join(PROJECT, "python", "outputs")
LOG_PATH  = os.path.join(OUTPUTS, "06_validate_report.txt")

log_lines = []

def log(text=""):
    print(text)
    log_lines.append(str(text))
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

def check(name, py_value, sql_value, tolerance=0.01):
    """Pass if py_value matches sql_value within tolerance (default 0.01)."""
    diff = abs(py_value - sql_value)
    status = "PASS" if diff <= tolerance else "FAIL"
    marker = "[ OK ]" if status == "PASS" else "[FAIL]"
    log(f"  {marker}  {name}")
    log(f"         Python = {py_value}")
    log(f"         SQL    = {sql_value}")
    log(f"         diff   = {diff:.6f}  (tolerance {tolerance})")
    return status == "PASS"

log("=" * 75)
log("STEP 6 — SQL vs PYTHON CROSS-CHECK")
log("=" * 75)
log(f"Python    : {sys.version.split()[0]}")
log(f"pandas    : {pd.__version__}")
log(f"Report    : {LOG_PATH}")
log()

results = []

# ============================================================================
# CHECK 1 — Track A overall attrition rate
# ============================================================================
log("=" * 75)
log("CHECK 1 — Track A overall attrition rate (SQL: A1a)")
log("=" * 75)
log()

drivers = pd.read_csv(os.path.join(PROCESSED, "master_driver_clean.csv"))
n_drivers = len(drivers)
n_leavers = int(drivers["driver_attrition"].sum())
rate = round(n_leavers * 100.0 / n_drivers, 2)

log(f"Loaded master_driver_clean.csv: {n_drivers} rows")
log(f"Python leavers: {n_leavers}")
log(f"Python rate   : {rate:.2f}%")
log()

ok_1 = check("driver count (150)",
             float(n_drivers), 150.0, tolerance=0.0)
results.append(ok_1)
ok_1b = check("leaver count (26)",
              float(n_leavers), 26.0, tolerance=0.0)
results.append(ok_1b)
ok_1c = check("attrition rate % (17.33)",
              rate, 17.33)
results.append(ok_1c)

# ============================================================================
# CHECK 2 — Track B delivery late rate
# ============================================================================
log()
log("=" * 75)
log("CHECK 2 — Track B delivery late rate (SQL: B1a)")
log("=" * 75)
log()

trips = pd.read_csv(os.path.join(PROCESSED, "master_trip_clean.csv"))
n_trips = len(trips)
n_late = int(trips["late_delivery_flag"].sum())
late_rate = round(n_late * 100.0 / n_trips, 2)

log(f"Loaded master_trip_clean.csv: {n_trips:,} rows")
log(f"Python late count : {n_late:,}")
log(f"Python late rate  : {late_rate:.2f}%")
log()

ok_2 = check("trip count (85410)",
             float(n_trips), 85410.0, tolerance=0.0)
results.append(ok_2)
ok_2b = check("late count (47308)",
              float(n_late), 47308.0, tolerance=0.0)
results.append(ok_2b)
ok_2c = check("late rate % (55.39)",
              late_rate, 55.39)
results.append(ok_2c)

# ============================================================================
# CHECK 3 — Track C preventive-maintenance cost (SQL: C5)
# ============================================================================
log()
log("=" * 75)
log("CHECK 3 — Track C preventive maintenance cost (SQL: C5)")
log("=" * 75)
log()

truck = pd.read_csv(os.path.join(PROCESSED, "master_truck_month_clean.csv"))
log(f"Loaded master_truck_month_clean.csv: {len(truck):,} rows")
log()

# Recreate C5's band definition exactly (same CASE expression as the SQL)
truck["preventive_band"] = pd.cut(
    truck["n_preventive"],
    bins=[-1, 0, 1, 3, 999],
    labels=["1. none", "2. one", "3. two-three", "4. four+"]
)
band_stats = truck.groupby("preventive_band", observed=True).agg(
    truck_months=("truck_id", "count"),
    avg_cost=("maintenance_cost", "mean"),
).reset_index()
band_stats["avg_cost"] = band_stats["avg_cost"].round(2)

log("Python band summary:")
log(band_stats.to_string(index=False))
log()

# Reconstruct SQL C5 values from the handoff
sql_c5 = {
    "1. none":      {"truck_months": 3010, "avg_cost": 1098.37},
    "2. one":       {"truck_months": 284,  "avg_cost": 3261.62},
    "3. two-three": {"truck_months": 18,   "avg_cost": 5390.42},
}

for band, sql_vals in sql_c5.items():
    py_row = band_stats[band_stats["preventive_band"] == band].iloc[0]
    ok_count = check(f"C5 {band} — truck_months ({sql_vals['truck_months']})",
                     float(py_row["truck_months"]), float(sql_vals["truck_months"]),
                     tolerance=0.0)
    results.append(ok_count)
    ok_cost = check(f"C5 {band} — avg_cost (${sql_vals['avg_cost']})",
                    float(py_row["avg_cost"]), float(sql_vals["avg_cost"]))
    results.append(ok_cost)

# ============================================================================
# CHECK 4 — Track C utilization anomaly profile (SQL: C8)
# ============================================================================
log()
log("=" * 75)
log("CHECK 4 — Track C utilization anomaly profile (SQL: C8)")
log("=" * 75)
log()

anomaly_stats = truck.groupby("utilization_over_100pct").agg(
    truck_months=("truck_id", "count"),
    avg_utilization_rate=("utilization_rate", "mean"),
    avg_total_miles=("total_miles", "mean"),
    avg_total_revenue=("total_revenue", "mean"),
    avg_maintenance_cost=("maintenance_cost", "mean"),
    avg_trips=("trips_completed", "mean"),
).round(2).reset_index()

log("Python anomaly summary:")
log(anomaly_stats.to_string(index=False))
log()

# SQL C8 values for the anomalous group (utilization_over_100pct = 1)
sql_c8_anomalous = {
    "truck_months": 436,
    "avg_utilization_rate": 1.11,
    "avg_total_miles": 48203,
    "avg_total_revenue": 103477,
    "avg_maintenance_cost": 1272.39,
    "avg_trips": 33.8,
}
py_anom = anomaly_stats[anomaly_stats["utilization_over_100pct"] == 1].iloc[0]

for col, sql_val in sql_c8_anomalous.items():
    if col == "avg_utilization_rate":
        tol = 0.01
    elif col in ("avg_total_miles", "avg_total_revenue"):
        tol = 1.0     # rounded to 0 in SQL
    elif col == "avg_trips":
        tol = 0.1
    else:
        tol = 0.01
    ok = check(f"C8 anomalous {col} (SQL {sql_val})",
               float(py_anom[col]), float(sql_val), tolerance=tol)
    results.append(ok)

# ============================================================================
# FINAL VERDICT
# ============================================================================
log()
log("=" * 75)
log("FINAL VERDICT")
log("=" * 75)
n_pass = sum(1 for r in results if r)
n_total = len(results)
log(f"Checks passed : {n_pass} / {n_total}")
log(f"Report saved  : {LOG_PATH}")
log()

if n_pass == n_total:
    log("STATUS: PASS — SQL and Python agree on all headline findings.")
    log("Step 6 complete. Step 7 (modelling) is safe to begin.")
    sys.exit(0)
else:
    log("STATUS: FAIL — SQL and Python disagree on at least one check.")
    log("DO NOT proceed to Step 7. Investigate the failing checks first.")
    sys.exit(1)