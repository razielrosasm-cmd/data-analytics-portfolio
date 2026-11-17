"""
02_clean_data.py — Step 3: Data Validation & Cleaning
Project: Logistics Operations Database (three-track charter)

Goal: Merge raw sources into three grain-consistent clean tables, preserve
all nulls (no imputation), preserve all original rows, produce an audit log
and a codebook. Rows are NEVER dropped here — listwise deletion happens only
inside modelling scripts.
"""

import pandas as pd
import os

# === CONFIG ===
PROJECT   = r"C:\Users\Anonymous\Desktop\projects\04-Logistics Operations Database"
RAW       = os.path.join(PROJECT, "data", "raw")
PROCESSED = os.path.join(PROJECT, "data", "processed")
OUTPUTS   = os.path.join(PROJECT, "python", "outputs")
DOCS      = os.path.join(PROJECT, "docs")

os.makedirs(PROCESSED, exist_ok=True)
os.makedirs(OUTPUTS,   exist_ok=True)
os.makedirs(DOCS,      exist_ok=True)

LOG_PATH = os.path.join(OUTPUTS, "02_clean_report.txt")
log_lines = []

def log(text=""):
    print(text)
    log_lines.append(str(text))
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

def read_raw(name, **kwargs):
    return pd.read_csv(os.path.join(RAW, name), **kwargs)

# === CODEBOOK BUILDER ===
codebook_rows = []

def add_codebook(table, df, specs):
    for col in df.columns:
        spec = specs.get(col, {})
        codebook_rows.append({
            "table":         table,
            "column":        col,
            "dtype":         str(df[col].dtype),
            "source_table":  spec.get("source", ""),
            "description":   spec.get("description", ""),
            "null_pct":      round(float(df[col].isnull().mean() * 100), 2),
            "is_target":     spec.get("is_target", False),
        })

# ============================================================================
# TRACK A — master_driver_clean.csv (1 row per driver, 150 rows)
# ============================================================================
log("=" * 75)
log("TRACK A — master_driver_clean.csv (1 row per driver)")
log("=" * 75)

drivers = read_raw("drivers.csv", parse_dates=["hire_date", "termination_date", "date_of_birth"])
log(f"Source drivers.csv: {len(drivers)} rows")
assert len(drivers) == 150, "Unexpected driver count — investigate before continuing"

# Target — deterministic from termination_date
drivers["driver_attrition"] = drivers["termination_date"].notna().astype(int)
log(f"Target driver_attrition: {int(drivers['driver_attrition'].sum())} leavers "
    f"/ {len(drivers)} total = {drivers['driver_attrition'].mean()*100:.2f}%")

# Derived features
drivers["hire_year"]   = drivers["hire_date"].dt.year
drivers["age_at_hire"] = ((drivers["hire_date"] - drivers["date_of_birth"]).dt.days / 365.25).round(1)

# Aggregate driver_monthly_metrics (36-month behaviour)
dmm = read_raw("driver_monthly_metrics.csv", parse_dates=["month"])
dmm_agg = dmm.groupby("driver_id").agg(
    n_months          =("month",              "count"),
    avg_on_time_rate  =("on_time_delivery_rate", "mean"),
    min_on_time_rate  =("on_time_delivery_rate", "min"),
    avg_mpg           =("average_mpg",        "mean"),
    total_trips_metered=("trips_completed",   "sum"),
    total_miles       =("total_miles",        "sum"),
    avg_idle_hours    =("average_idle_hours", "mean"),
    n_low_ontime_months=("on_time_delivery_rate", lambda x: int((x < 0.5).sum())),
).reset_index()

# Anomaly flag for the 38% puzzle
dmm_agg["has_low_ontime_month"] = (dmm_agg["n_low_ontime_months"] > 0).astype(int)

# Aggregate trips (where driver was assigned)
trips = read_raw("trips.csv", parse_dates=["dispatch_date"])
trips_assigned = trips.dropna(subset=["driver_id"]).copy()
trips_agg = trips_assigned.groupby("driver_id").agg(
    n_trips_assigned   =("trip_id",               "count"),
    total_distance     =("actual_distance_miles", "sum"),
    avg_idle_from_trips=("idle_time_hours",       "mean"),
    avg_mpg_from_trips =("average_mpg",           "mean"),
).reset_index()

# Aggregate safety_incidents
safety = read_raw("safety_incidents.csv")
safety_assigned = safety.dropna(subset=["driver_id"]).copy()
safety_agg = safety_assigned.groupby("driver_id").agg(
    n_incidents  =("incident_id",     "count"),
    n_at_fault   =("at_fault_flag",   "sum"),
    n_preventable=("preventable_flag","sum"),
    total_claim  =("claim_amount",    "sum"),
).reset_index()

# Merge — left joins preserve all 150 drivers
driver_master = drivers.merge(dmm_agg,     on="driver_id", how="left")
driver_master = driver_master.merge(trips_agg,  on="driver_id", how="left")
driver_master = driver_master.merge(safety_agg, on="driver_id", how="left")
assert len(driver_master) == 150, "Row count changed on Track A merge"

# Structural zeros (facts, not imputation): a driver with no events HAS 0 events
for col in ["n_trips_assigned", "total_distance",
            "n_incidents", "n_at_fault", "n_preventable", "total_claim"]:
    driver_master[col] = driver_master[col].fillna(0)

# Select final columns — drop PII
driver_master = driver_master[[
    "driver_id", "hire_date", "termination_date", "driver_attrition",
    "hire_year", "age_at_hire", "years_experience", "cdl_class",
    "employment_status", "home_terminal",
    "n_months", "avg_on_time_rate", "min_on_time_rate", "avg_mpg",
    "total_trips_metered", "total_miles", "avg_idle_hours",
    "n_low_ontime_months", "has_low_ontime_month",
    "n_trips_assigned", "total_distance",
    "avg_idle_from_trips", "avg_mpg_from_trips",
    "n_incidents", "n_at_fault", "n_preventable", "total_claim",
]].sort_values("driver_id").reset_index(drop=True)

driver_master.to_csv(os.path.join(PROCESSED, "master_driver_clean.csv"), index=False)
log(f"Final master_driver_clean.csv: {len(driver_master)} rows, {len(driver_master.columns)} columns")
log("Null counts per column:")
log(driver_master.isnull().sum().to_string())

add_codebook("master_driver_clean", driver_master, {
    "driver_id":           {"source": "drivers",                     "description": "Driver primary key"},
    "hire_date":           {"source": "drivers",                     "description": "Original hire date"},
    "termination_date":    {"source": "drivers",                     "description": "Termination date; null = still employed"},
    "driver_attrition":    {"source": "derived (termination_date not null)", "description": "Target: 1 = left company, 0 = active", "is_target": True},
    "hire_year":           {"source": "derived (hire_date.year)",    "description": "Year driver was hired"},
    "age_at_hire":         {"source": "derived (hire_date - date_of_birth)", "description": "Age at hire (years)"},
    "years_experience":    {"source": "drivers",                     "description": "Years of driving experience at hire"},
    "cdl_class":           {"source": "drivers",                     "description": "Commercial driver license class"},
    "employment_status":   {"source": "drivers",                     "description": "Current employment status"},
    "home_terminal":       {"source": "drivers",                     "description": "Home terminal city"},
    "n_months":            {"source": "agg driver_monthly_metrics",  "description": "Number of months with recorded metrics"},
    "avg_on_time_rate":    {"source": "agg driver_monthly_metrics",  "description": "Mean monthly on-time delivery rate"},
    "min_on_time_rate":    {"source": "agg driver_monthly_metrics",  "description": "Worst single-month on-time rate"},
    "avg_mpg":             {"source": "agg driver_monthly_metrics",  "description": "Mean monthly MPG"},
    "total_trips_metered": {"source": "agg driver_monthly_metrics",  "description": "Sum of monthly trips completed"},
    "total_miles":         {"source": "agg driver_monthly_metrics",  "description": "Sum of monthly miles"},
    "avg_idle_hours":      {"source": "agg driver_monthly_metrics",  "description": "Mean monthly idle hours"},
    "n_low_ontime_months": {"source": "agg driver_monthly_metrics",  "description": "Months with on-time rate below 50% (anomaly count)"},
    "has_low_ontime_month":{"source": "derived",                     "description": "1 if driver ever had a month below 50% on-time"},
    "n_trips_assigned":    {"source": "agg trips",                   "description": "Trips with this driver assigned"},
    "total_distance":      {"source": "agg trips",                   "description": "Sum of actual_distance_miles"},
    "avg_idle_from_trips": {"source": "agg trips",                   "description": "Mean idle_time_hours per trip"},
    "avg_mpg_from_trips":  {"source": "agg trips",                   "description": "Mean average_mpg per trip"},
    "n_incidents":         {"source": "agg safety_incidents",        "description": "Number of safety incidents"},
    "n_at_fault":          {"source": "agg safety_incidents",        "description": "Incidents where driver was at fault"},
    "n_preventable":       {"source": "agg safety_incidents",        "description": "Preventable incidents"},
    "total_claim":         {"source": "agg safety_incidents",        "description": "Total claim amount USD"},
})

# ============================================================================
# TRACK B — master_trip_clean.csv (1 row per trip/load, 85,410 rows)
# ============================================================================
log("")
log("=" * 75)
log("TRACK B — master_trip_clean.csv (1 row per trip/load)")
log("=" * 75)

loads     = read_raw("loads.csv",     parse_dates=["load_date"])
trips_b   = read_raw("trips.csv",     parse_dates=["dispatch_date"])
routes    = read_raw("routes.csv")
customers = read_raw("customers.csv", parse_dates=["contract_start_date"])
de        = read_raw("delivery_events.csv", parse_dates=["scheduled_datetime", "actual_datetime"])

# Split delivery_events
pickup = de[de["event_type"] == "Pickup"][
    ["load_id", "on_time_flag", "detention_minutes"]
].rename(columns={"on_time_flag": "pickup_on_time_flag",
                  "detention_minutes": "pickup_detention_minutes"})

delivery = de[de["event_type"] == "Delivery"][
    ["load_id", "on_time_flag", "detention_minutes"]
].rename(columns={"on_time_flag": "delivery_on_time_flag",
                  "detention_minutes": "delivery_detention_minutes"})

# Defensive: dedup if any load has duplicate events (should be 0)
if pickup["load_id"].duplicated().any():
    log(f"WARNING: pickup has {int(pickup['load_id'].duplicated().sum())} duplicate load_ids — keeping first")
    pickup = pickup.drop_duplicates(subset="load_id", keep="first")
if delivery["load_id"].duplicated().any():
    log(f"WARNING: delivery has {int(delivery['load_id'].duplicated().sum())} duplicate load_ids — keeping first")
    delivery = delivery.drop_duplicates(subset="load_id", keep="first")

log(f"Pickup events after dedup: {len(pickup)}")
log(f"Delivery events after dedup: {len(delivery)}")

# Targets and features
delivery["late_delivery_flag"] = (~delivery["delivery_on_time_flag"]).astype(int)
pickup["pickup_late_flag"]     = (~pickup["pickup_on_time_flag"]).astype(int)

# Merge — base is loads (85,410 rows); all joins must preserve row count
trip_master = loads.merge(trips_b, on="load_id", how="left")
assert len(trip_master) == len(loads), f"Row inflation on trips merge: {len(loads)} -> {len(trip_master)}"

trip_master = trip_master.merge(routes, on="route_id", how="left")
trip_master = trip_master.merge(
    customers[["customer_id", "customer_type", "credit_terms_days", "primary_freight_type"]],
    on="customer_id", how="left"
)
trip_master = trip_master.merge(pickup,   on="load_id", how="left")
trip_master = trip_master.merge(delivery, on="load_id", how="left")
assert len(trip_master) == len(loads), f"Row inflation after all merges: {len(loads)} -> {len(trip_master)}"

n_known  = int(trip_master["late_delivery_flag"].notna().sum())
n_late   = int(trip_master["late_delivery_flag"].sum())
log(f"Target late_delivery_flag: {n_late} late / {n_known} with target = "
    f"{n_late / max(n_known,1) * 100:.2f}%")
log(f"Rows with unknown target (no matching delivery event): "
    f"{int(trip_master['late_delivery_flag'].isnull().sum())}")

trip_master = trip_master[[
    "load_id", "load_date", "load_type", "weight_lbs", "pieces",
    "revenue", "fuel_surcharge", "accessorial_charges",
    "load_status", "booking_type",
    "trip_id", "driver_id", "truck_id", "trailer_id",
    "dispatch_date", "actual_distance_miles", "actual_duration_hours",
    "fuel_gallons_used", "average_mpg", "idle_time_hours", "trip_status",
    "route_id", "origin_city", "destination_city",
    "typical_distance_miles", "base_rate_per_mile", "typical_transit_days",
    "customer_id", "customer_type", "credit_terms_days", "primary_freight_type",
    "pickup_on_time_flag", "pickup_detention_minutes", "pickup_late_flag",
    "delivery_on_time_flag", "delivery_detention_minutes", "late_delivery_flag",
]].sort_values("load_id").reset_index(drop=True)

trip_master.to_csv(os.path.join(PROCESSED, "master_trip_clean.csv"), index=False)
log(f"Final master_trip_clean.csv: {len(trip_master)} rows, {len(trip_master.columns)} columns")
log("Null counts (columns with >0 nulls):")
nulls_b = trip_master.isnull().sum()
log(nulls_b[nulls_b > 0].to_string())

add_codebook("master_trip_clean", trip_master, {
    "load_id":                  {"source": "loads",             "description": "Load primary key"},
    "load_date":                {"source": "loads",             "description": "Date load was booked"},
    "load_type":                {"source": "loads",             "description": "Dry Van / Refrigerated / etc."},
    "weight_lbs":               {"source": "loads",             "description": "Cargo weight (pounds)"},
    "pieces":                   {"source": "loads",             "description": "Number of pieces"},
    "revenue":                  {"source": "loads",             "description": "Load revenue (USD)"},
    "fuel_surcharge":           {"source": "loads",             "description": "Fuel surcharge (USD)"},
    "accessorial_charges":      {"source": "loads",             "description": "Extra charges (USD)"},
    "load_status":              {"source": "loads",             "description": "Completed / Cancelled / etc."},
    "booking_type":             {"source": "loads",             "description": "Spot or Dedicated"},
    "trip_id":                  {"source": "trips",             "description": "Trip primary key"},
    "driver_id":                {"source": "trips",             "description": "Assigned driver; null = unassigned (2.01%)"},
    "truck_id":                 {"source": "trips",             "description": "Assigned truck; null = unassigned (1.96%)"},
    "trailer_id":               {"source": "trips",             "description": "Assigned trailer; null = unassigned (1.97%)"},
    "dispatch_date":            {"source": "trips",             "description": "Trip dispatch date"},
    "actual_distance_miles":    {"source": "trips",             "description": "Distance driven"},
    "actual_duration_hours":    {"source": "trips",             "description": "Trip duration"},
    "fuel_gallons_used":        {"source": "trips",             "description": "Fuel consumed"},
    "average_mpg":              {"source": "trips",             "description": "Trip MPG"},
    "idle_time_hours":          {"source": "trips",             "description": "Idle hours during trip"},
    "trip_status":              {"source": "trips",             "description": "Completed / Cancelled / etc."},
    "route_id":                 {"source": "routes",            "description": "Lane primary key"},
    "origin_city":              {"source": "routes",            "description": "Origin city"},
    "destination_city":         {"source": "routes",            "description": "Destination city"},
    "typical_distance_miles":   {"source": "routes",            "description": "Lane typical distance"},
    "base_rate_per_mile":       {"source": "routes",            "description": "Lane base rate"},
    "typical_transit_days":     {"source": "routes",            "description": "Lane scheduled transit"},
    "customer_id":              {"source": "customers",         "description": "Customer primary key"},
    "customer_type":            {"source": "customers",         "description": "Contract / Dedicated / etc."},
    "credit_terms_days":        {"source": "customers",         "description": "Customer payment terms"},
    "primary_freight_type":     {"source": "customers",         "description": "Customer freight category"},
    "pickup_on_time_flag":      {"source": "delivery_events",   "description": "Pickup on-time (True/False); null if no pickup event"},
    "pickup_detention_minutes": {"source": "delivery_events",   "description": "Pickup detention minutes"},
    "pickup_late_flag":         {"source": "derived",           "description": "1 = pickup was late"},
    "delivery_on_time_flag":    {"source": "delivery_events",   "description": "Delivery on-time (True/False)"},
    "delivery_detention_minutes":{"source": "delivery_events",  "description": "Delivery detention minutes"},
    "late_delivery_flag":       {"source": "derived",           "description": "Target: 1 = delivery was late, 0 = on time", "is_target": True},
})

# ============================================================================
# TRACK C — master_truck_month_clean.csv (1 row per truck-month, 3,312 rows)
# ============================================================================
log("")
log("=" * 75)
log("TRACK C — master_truck_month_clean.csv (1 row per truck-month)")
log("=" * 75)

trucks = read_raw("trucks.csv", parse_dates=["acquisition_date"])
tum    = read_raw("truck_utilization_metrics.csv", parse_dates=["month"])
maint  = read_raw("maintenance_records.csv",        parse_dates=["maintenance_date"])

# Compute threshold FIRST and log it
threshold_75 = float(tum["maintenance_cost"].quantile(0.75))
log(f"75th percentile of maintenance_cost across {len(tum)} truck-months = ${threshold_75:,.2f}")
if threshold_75 == 0:
    log("WARNING: 75th percentile is $0 — high_maintenance_flag will be degenerate. ESCALATE.")

tum["high_maintenance_flag"]  = (tum["maintenance_cost"] >= threshold_75).astype(int)
tum["utilization_over_100pct"] = (tum["utilization_rate"] > 1.0).astype(int)

log(f"Target high_maintenance_flag: {int(tum['high_maintenance_flag'].sum())} positive "
    f"/ {len(tum)} = {tum['high_maintenance_flag'].mean()*100:.2f}%")
log(f"Anomaly utilization_rate > 1.0: {int(tum['utilization_over_100pct'].sum())} rows "
    f"({tum['utilization_over_100pct'].mean()*100:.2f}%)")

# Aggregate maintenance to truck-month
maint["month"] = maint["maintenance_date"].dt.to_period("M").dt.to_timestamp()
maint_agg = maint.groupby(["truck_id", "month"]).agg(
    n_maintenance_records=("maintenance_id",   "count"),
    n_preventive         =("maintenance_type", lambda x: int((x == "Preventive").sum())),
    avg_odometer         =("odometer_reading", "mean"),
).reset_index()

# Diagnostic: maintenance months with no utilization record (excluded from clean table)
maint_pairs = set(zip(maint_agg["truck_id"], maint_agg["month"]))
tum_pairs   = set(zip(tum["truck_id"],       tum["month"]))
log(f"Truck-months with maintenance but no utilization record (excluded): "
    f"{len(maint_pairs - tum_pairs)}")

# Merge
truck_master = tum.merge(trucks, on="truck_id", how="left")
assert len(truck_master) == len(tum), "Row inflation on trucks merge"

truck_master = truck_master.merge(maint_agg, on=["truck_id", "month"], how="left")
assert len(truck_master) == len(tum), "Row inflation on maintenance merge"

# Structural zeros
for col in ["n_maintenance_records", "n_preventive"]:
    truck_master[col] = truck_master[col].fillna(0)

truck_master["truck_age_years"] = (
    (truck_master["month"] - truck_master["acquisition_date"]).dt.days / 365.25
).round(2)

# Reconciliation check
recon_gap = (truck_master["maintenance_events"] - truck_master["n_maintenance_records"]).abs()
n_mismatch = int((recon_gap > 0).sum())
log(f"Reconciliation: truck-months where maintenance_events != n_maintenance_records = "
    f"{n_mismatch} (of {len(truck_master)})")

truck_master = truck_master[[
    "truck_id", "month",
    "trips_completed", "total_miles", "total_revenue", "average_mpg",
    "maintenance_events", "maintenance_cost", "downtime_hours", "utilization_rate",
    "high_maintenance_flag", "utilization_over_100pct",
    "make", "model_year", "acquisition_date", "acquisition_mileage",
    "fuel_type", "tank_capacity_gallons", "status", "home_terminal",
    "truck_age_years",
    "n_maintenance_records", "n_preventive", "avg_odometer",
]].sort_values(["truck_id", "month"]).reset_index(drop=True)

truck_master.to_csv(os.path.join(PROCESSED, "master_truck_month_clean.csv"), index=False)
log(f"Final master_truck_month_clean.csv: {len(truck_master)} rows, {len(truck_master.columns)} columns")
log("Null counts (columns with >0 nulls):")
nulls_c = truck_master.isnull().sum()
log(nulls_c[nulls_c > 0].to_string())

add_codebook("master_truck_month_clean", truck_master, {
    "truck_id":                {"source": "truck_utilization_metrics", "description": "Truck primary key"},
    "month":                   {"source": "truck_utilization_metrics", "description": "Month start (first of month)"},
    "trips_completed":         {"source": "truck_utilization_metrics", "description": "Trips in month"},
    "total_miles":             {"source": "truck_utilization_metrics", "description": "Miles in month"},
    "total_revenue":           {"source": "truck_utilization_metrics", "description": "Revenue in month"},
    "average_mpg":             {"source": "truck_utilization_metrics", "description": "Mean MPG in month"},
    "maintenance_events":      {"source": "truck_utilization_metrics", "description": "Maintenance event count from source"},
    "maintenance_cost":        {"source": "truck_utilization_metrics", "description": "Maintenance cost USD"},
    "downtime_hours":          {"source": "truck_utilization_metrics", "description": "Downtime hours"},
    "utilization_rate":        {"source": "truck_utilization_metrics", "description": "Utilization (can exceed 1.0)"},
    "high_maintenance_flag":   {"source": "derived (>=75th pct)",     "description": "Target: 1 = top-quartile cost month", "is_target": True},
    "utilization_over_100pct": {"source": "derived (utilization > 1.0)", "description": "Anomaly flag for utilization_rate > 1.0"},
    "make":                    {"source": "trucks",                   "description": "Truck make (e.g. Peterbilt)"},
    "model_year":              {"source": "trucks",                   "description": "Model year"},
    "acquisition_date":        {"source": "trucks",                   "description": "Purchase date"},
    "acquisition_mileage":     {"source": "trucks",                   "description": "Odometer at purchase"},
    "fuel_type":               {"source": "trucks",                   "description": "Diesel etc."},
    "tank_capacity_gallons":   {"source": "trucks",                   "description": "Tank size"},
    "status":                  {"source": "trucks",                   "description": "Active / Maintenance / etc."},
    "home_terminal":           {"source": "trucks",                   "description": "Home terminal city"},
    "truck_age_years":         {"source": "derived (month - acquisition_date)", "description": "Truck age at month"},
    "n_maintenance_records":   {"source": "agg maintenance_records",  "description": "Count of maintenance events in month"},
    "n_preventive":            {"source": "agg maintenance_records",  "description": "Preventive maintenance count"},
    "avg_odometer":            {"source": "agg maintenance_records",  "description": "Mean odometer at maintenance"},
})

# ============================================================================
# CODEBOOK EXPORT + FINAL SUMMARY
# ============================================================================
log("")
log("=" * 75)
log("CODEBOOK AND FINAL SUMMARY")
log("=" * 75)

codebook_df = pd.DataFrame(codebook_rows)
codebook_df.to_csv(os.path.join(DOCS, "codebook.csv"), index=False)
log(f"Codebook saved: {len(codebook_df)} column entries across 3 tables")
log(f"  -> {os.path.join(DOCS, 'codebook.csv')}")

log("")
log("PER-TABLE SUMMARY")
summary = pd.DataFrame([
    {"table": "master_driver_clean",      "rows": len(driver_master), "cols": len(driver_master.columns), "target": "driver_attrition",     "positive_rate_pct": round(driver_master["driver_attrition"].mean()*100, 2)},
    {"table": "master_trip_clean",        "rows": len(trip_master),   "cols": len(trip_master.columns),   "target": "late_delivery_flag",  "positive_rate_pct": round(trip_master["late_delivery_flag"].dropna().mean()*100, 2)},
    {"table": "master_truck_month_clean", "rows": len(truck_master),  "cols": len(truck_master.columns),  "target": "high_maintenance_flag","positive_rate_pct": round(truck_master["high_maintenance_flag"].mean()*100, 2)},
])
log(summary.to_string(index=False))

log("")
log(f"Audit log: {LOG_PATH}")
log("Step 3 complete. All rows preserved. No imputation performed.")