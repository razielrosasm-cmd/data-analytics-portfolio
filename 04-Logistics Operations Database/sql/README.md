# SQL Analysis — Logistics Operations Database

> 28 independent queries across three analytical tracks, validating 
> whether driver attrition, on-time delivery, and maintenance costs 
> contain actionable signals.

[![SQL](https://img.shields.io/badge/SQL-SQLite-blue)]()

---

## Overview

This folder contains the SQLite database, the Python script used to load the data, and the 28 analysis queries that drove the findings on the dashboard. 

All queries are written in standard SQLite SQL and are organized by analytical track (A, B, and C).

---

## Folder Structure

- **`db/`** — The generated SQLite database (`logistics.db`)
- **`analysis/`** — 28 SQL queries, organized by track prefix (`track_a_`, `track_b_`, `track_c_`)
- **`results/`** — CSV exports of every query result, used for validation and documentation
- **`load_data.py`** — Python script to build the SQLite database from the processed CSVs
- **`schema.sql`** — The exact table definitions and data types

---

## How to Run the Database

To rebuild the database from scratch:

1. Ensure the cleaned CSV files exist in `data/processed/` (run the Python cleaning script first if they do not).
2. Navigate to this folder and run the loader:
   `cd sql`
   `python load_data.py`
3. The script will create `db/logistics.db` and populate it with the three master tables.

---

## The 28 Analysis Queries

The analysis is divided into three tracks. Each track answers a specific operational question for the Logistics Supervisor.

### Track A — Driver Attrition (11 Queries)

**Objective:** Determine if driver turnover can be predicted by experience, terminal, or safety records.
**Result:** All tests returned flat. Turnover does not correlate with any available behavioural or operational metric. 

| Query File | What It Tests |
|---|---|
| `track_a_01a_overall.sql` | Baseline attrition rate across the entire fleet |
| `track_a_01b_hire_year.sql` | Turnover broken down by the year drivers were hired |
| `track_a_01c_status_check.sql` | Verifies active vs. terminated statuses in the system |
| `track_a_02_by_terminal.sql` | Turnover rate by home terminal |
| `track_a_03_by_cdl.sql` | Turnover rate by CDL license class |
| `track_a_04_by_experience.sql` | Turnover rate by years of experience |
| `track_a_05_by_safety.sql` | Turnover rate by safety incident history |
| `track_a_06_performance.sql` | Links turnover to performance metrics |
| `track_a_07_high_risk_cell.sql` | Tests for intersections (e.g., low experience + high safety incidents) |
| `track_a_08_no_metrics_puzzle.sql` | Proves departing drivers have no behavioural records |
| `track_a_09_cohort_survival.sql` | Time-to-leave survival analysis by cohort |

### Track B — On-Time Delivery (10 Queries)

**Objective:** Identify which operational segments cause late deliveries.
**Result:** The late rate is universally flat at **54–57%** across all 28 independent tests. No operational signal exists.

| Query File | What It Tests |
|---|---|
| `track_b_01a_vendor_claim.sql` | Tests the vendor's claim of 85-95% on-time delivery |
| `track_b_01_baseline.sql` | Baseline late-delivery rate across all trips |
| `track_b_02_pickup_vs_delivery.sql` | Late at pickup vs. late at delivery |
| `track_b_03_by_route.sql` | Late rate by specific route |
| `track_b_04_by_customer_type.sql` | Late rate by customer segment |
| `track_b_05_by_booking_type.sql` | Late rate by booking method (e.g., app vs. manual) |
| `track_b_06_by_distance_band.sql` | Late rate by trip distance |
| `track_b_07_by_detention.sql` | Late rate by time spent waiting at facilities |
| `track_b_08_by_idle.sql` | Late rate by truck idle time |
| `track_b_09_high_risk_cell.sql` | Tests intersections (e.g., long distance + high detention) |
| `track_b_10_by_month.sql` | Tests for seasonality (month-over-month late rates) |

### Track C — Maintenance (7 Queries)

**Objective:** Identify the true drivers of high-cost maintenance months.
**Result:** **Actionable.** Two factors dominate: preventive shop visits (12.5x higher odds) and downtime hours (7.6% higher odds per hour).

| Query File | What It Tests |
|---|---|
| `track_c_01_baseline.sql` | Baseline maintenance cost per truck-month |
| `track_c_02_by_make.sql` | Cost differences by truck manufacturer |
| `track_c_03_by_age_band.sql` | Cost differences by vehicle age |
| `track_c_04_by_miles_band.sql` | Cost differences by total miles driven |
| `track_c_05_preventive.sql` | Cost impact of preventive maintenance visits |
| `track_c_06_downtime.sql` | Cost impact of shop downtime hours |
| `track_c_07_high_risk_cell.sql` | Tests intersections of high-cost factors |
| `track_c_08_utilization_anomaly.sql` | Checks if extreme usage predicts cost |

---

## Data Export

Every query in the `analysis/` folder has a corresponding CSV export in the `results/` folder. 

These CSVs were used to build the dashboard charts and validate the Python logistic regression model. You can view the exact numbers behind every visual without needing to run the SQL yourself.

---

## Schema Overview

The database contains three main tables:

- **`driver`** — One row per driver (includes hire date, terminal, safety incidents, and attrition status)
- **`trip`** — One row per trip (includes distance, route, customer type, and on-time flags)
- **`truck_month`** — One row per truck per month (includes maintenance cost, preventive visits, downtime hours, and miles driven). **This is the core table for the actionable Track C analysis.**