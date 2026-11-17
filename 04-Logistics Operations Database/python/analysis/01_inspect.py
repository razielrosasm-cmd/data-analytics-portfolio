import pandas as pd
import os

# === CONFIG ===
RAW_DIR    = r"C:\Users\Anonymous\Desktop\projects\04-Logistics Operations Database\data\raw"
OUTPUT_DIR = r"C:\Users\Anonymous\Desktop\projects\04-Logistics Operations Database\python\outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FILES = [
    "customers.csv", "delivery_events.csv", "driver_monthly_metrics.csv",
    "drivers.csv", "facilities.csv", "fuel_purchases.csv", "loads.csv",
    "maintenance_records.csv", "routes.csv", "safety_incidents.csv",
    "trailers.csv", "trips.csv", "truck_utilization_metrics.csv", "trucks.csv"
]

log_path = os.path.join(OUTPUT_DIR, "01_inspect_report.txt")
log = open(log_path, "w", encoding="utf-8")

def p(text=""):
    print(text)
    log.write(str(text) + "\n")

summary_rows = []

for fname in FILES:
    df = pd.read_csv(os.path.join(RAW_DIR, fname))

    p("=" * 75)
    p(f"FILE: {fname}")
    p("=" * 75)
    p(f"Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    p("")
    p("Dtypes:")
    p(df.dtypes.to_string())
    p("")

    nulls = df.isnull().sum()
    nulls_nonzero = nulls[nulls > 0]
    if len(nulls_nonzero) > 0:
        p("Columns with nulls:")
        null_report = pd.DataFrame({
            "null_count": nulls_nonzero,
            "null_pct":   (nulls_nonzero / len(df) * 100).round(2)
        })
        p(null_report.to_string())
    else:
        p("Nulls: none detected.")
    p("")

    p("Sample (first 3 rows):")
    p(df.head(3).to_string())
    p("")

    summary_rows.append({
        "file":            fname,
        "rows":            df.shape[0],
        "columns":         df.shape[1],
        "cols_with_nulls": int((nulls > 0).sum())
    })

p("=" * 75)
p("SUMMARY TABLE")
p("=" * 75)
p(pd.DataFrame(summary_rows).to_string(index=False))

log.close()
print(f"\nReport saved to: {log_path}")