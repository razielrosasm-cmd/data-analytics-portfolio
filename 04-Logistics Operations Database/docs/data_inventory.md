# Data Inventory — Logistics Operations Database

Governance document. Records the size, grain, and integrity status of every
table used in the analysis, plus every exclusion decision made during cleaning.

## Project context

Fictional Class 8 trucking company, operations 2022–2024. Fourteen raw CSVs in
`data/raw/`, three grain-consistent clean tables in `data/processed/`, one
SQLite database in `sql/db/logistics.db`. Three analytical tracks (driver
attrition, on-time delivery, maintenance) run in parallel on the same pipeline.

## Source dataset — verification against vendor claim

The Kaggle page claims *"85,000+ records across 14 interconnected tables"*. The
raw data was counted independently during Step 2 and the actual total is
**~549,700 records** — roughly **6.5×** the claim. This inventory uses verified
counts, not vendor claims.

| Raw table | Verified rows |
|---|---|
| customers | 200 |
| delivery_events | 170,820 |
| driver_monthly_metrics | 4,464 |
| drivers | 150 |
| facilities | 50 |
| fuel_purchases | 196,442 |
| loads | 85,410 |
| maintenance_records | 2,920 |
| routes | 58 |
| safety_incidents | 170 |
| trailers | 180 |
| trips | 85,410 |
| truck_utilization_metrics | 3,312 |
| trucks | 120 |
| **Total** | **549,706** |

## Clean tables — one per analytical track

### `master_driver_clean.csv` — Track A (Driver Attrition)

- **Grain:** one row per driver.
- **Rows:** **150** (no rows dropped, no rows added).
- **Target:** `driver_attrition`, defined as `termination_date IS NOT NULL`. Base rate **17.33%** (26 leavers / 150 drivers).
- **Sources:** `drivers` (base), aggregated `driver_monthly_metrics`, aggregated `trips`, aggregated `safety_incidents`.
- **Nulls preserved:** `termination_date` (124 nulls = the 82.67% active drivers) plus **26 nulls in every behavioural column** — the 26 terminated drivers have no monthly metrics in the source. This is a structural property of the dataset and will require an explicit modelling strategy in Step 7.
- **PII removed:** `license_number`, `license_state`, `date_of_birth` are dropped from the clean table. `age_at_hire` is retained as a derived feature.

### `master_trip_clean.csv` — Track B (On-Time Delivery)

- **Grain:** one row per trip/load (1:1 join between `loads` and `trips`).
- **Rows:** **85,410** (no rows dropped, no rows added).
- **Target:** `late_delivery_flag = 1` if the delivery event's `on_time_flag = 0`. Base rate **55.39%** (47,308 late / 85,410 trips).
- **Sources:** `loads` (base), `trips`, `routes`, `customers`, `delivery_events` (split into pickup and delivery, one each per load).
- **Nulls preserved:** `driver_id` (1,714 nulls, 2.01%), `truck_id` (1,672, 1.96%), `trailer_id` (1,680, 1.97%). These are intentional operational gaps. Listwise deletion happens inside the Track B model, not here.
- **Observed service level (55.39% late) vs vendor claim (85–95% on-time):** flagged as a finding to investigate in Step 5.

### `master_truck_month_clean.csv` — Track C (Maintenance)

- **Grain:** one row per truck-month, as defined by `truck_utilization_metrics.csv`.
- **Rows:** **3,312** (no rows dropped, no rows added).
- **Target:** `high_maintenance_flag = 1` if `maintenance_cost >= $2,409.79`, the 75th percentile of `maintenance_cost` across all 3,312 truck-months. Base rate **25.00%** by construction.
- **Sources:** `truck_utilization_metrics` (base), `trucks`, aggregated `maintenance_records`.
- **Nulls preserved:** `avg_odometer` (1,684 nulls, 50.8%) — truck-months with no maintenance record have no odometer reading. Not imputed.
- **Anomalies flagged but not fixed:** `utilization_over_100pct` — 436 rows (13.16%) report utilization above 1.0. This is preserved and flagged for Step 5 investigation.

### Excluded rows — maintenance-only truck-months

**501 truck-months** appear in `maintenance_records` with a `(truck_id, month)` pair that does not exist in `truck_utilization_metrics`. They are **excluded from `master_truck_month_clean.csv`** for two reasons:

1. **No utilization features exist for them.** Rows would be entirely null on the utilization side, making them unusable as predictors.

2. **Target leakage by construction.** These months exist in the maintenance table *because* maintenance happened. Including them would make "high-maintenance month" partly defined by the inclusion rule itself — the model would learn to predict maintenance from maintenance.

The 501 rows remain in `data/raw/maintenance_records.csv` and are cited as a data-quality gap in Track C's Limitations. A reconciliation check (see below) confirms they are the *only* excluded rows.

## Data-quality verifications performed

- **Foreign key integrity:** every `load_id` in `trips` matches a `load_id` in `loads`; every `trip_id` in `delivery_events` matches a `trip_id` in `trips`. Confirmed during the Step 3 merges via row-count assertions that did not fail.

- **Delivery event completeness:** 170,820 events ÷ 85,410 loads = **exactly 2.00 events per load** — one pickup, one delivery. No orphan or duplicate events.

- **Maintenance reconciliation (utilization rows only):** `maintenance_events` in `truck_utilization_metrics` equals the count of raw `maintenance_records` for that truck-month, across all 3,312 rows. **0 mismatches.** This confirms the utilization table's maintenance rollup is complete for the rows it covers, and that the 501 excluded rows are a separate population (not missing data from the rollup).

## Rules applied throughout (frozen)

- **No imputation** of nulls.
- **No row deletions** from original sources.
- **All nulls preserved** in the clean tables.
- **Listwise deletion happens only inside modelling scripts**, never in cleaning.
- **Structural zeros** filled only for facts (e.g., a driver with 0 incidents has 0 incidents).