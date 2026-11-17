# Data Cleaning Log — Logistics Operations Database

This document records the transformations, merges, and data quality decisions applied to the 16 raw CSV files to create the three analytical master tables. 

All cleaning was performed via `python/analysis/02_clean_data.py`. 

---

## Cleaning Philosophy

- **Preserve the raw data:** Source files in `data/raw/` are never modified.

- **No silent drops:** If rows are removed, the reason is documented here and in `outputs/02_clean_report.txt`.

- **Impute with logic:** Missing values are imputed only when a business rule exists (e.g., missing mileage is calculated from known route distance). Otherwise, they remain null.

---

## Master Table 1: `master_driver_clean.csv`

**Source Tables:** `drivers.csv`, `driver_monthly_metrics.csv`, `safety_incidents.csv`

**Goal:** One row per driver, containing their profile, safety history, and attrition status.

### Cleaning Steps & Decisions:

1. **Deduplication:** No duplicate driver IDs were found.

2. **Date Parsing:** `hire_date` and `termination_date` were converted to standard ISO 8601 format (`YYYY-MM-DD`). 

3. **Attrition Flag:** Created a binary `is_leaver` column (1 if `termination_date` is not null, 0 otherwise).

4. **Safety Incidents:** Aggregated `safety_incidents.csv` to count total incidents per driver, then joined to the main driver table. Missing incident records were imputed as `0` (no known incidents).

5. **Behavioural Records:** All 26 leavers were confirmed to have zero records in `driver_monthly_metrics.csv`. This is a core finding of Track A, not a cleaning error.

---

## Master Table 2: `master_trip_clean.csv`

**Source Tables:** `trips.csv`, `routes.csv`, `loads.csv`, `customers.csv`, `delivery_events.csv`

**Goal:** One row per trip, containing distance, customer type, and on-time performance flags.

### Cleaning Steps & Decisions:

1. **Date Parsing:** Pickup and delivery timestamps were standardised.

2. **Joining Routes & Customers:** Joined `route_id` and `customer_id` to pull in `distance_band`, `customer_type`, and `booking_type`.

3. **On-Time Flag:** Calculated `is_late` (1 if actual delivery > scheduled delivery + tolerance window). The tolerance window was determined based on standard industry practice (30 minutes).

4. **Distance Handling:** Confirmed `actual_distance_miles` is numeric. Handled missing values by falling back to the route's planned distance. 

5. **Detention & Idle Time:** Aggregated `delivery_events.csv` to calculate total wait time per trip. Nulls were handled as `0` wait time.

---

## Master Table 3: `master_truck_month_clean.csv`

**Source Tables:** `trucks.csv`, `truck_utilization_metrics.csv`, `maintenance_records.csv`, `fuel_purchases.csv`

**Goal:** One row per truck per month (3,312 rows total). This is the core table for the actionable Track C analysis.

### Cleaning Steps & Decisions:

1. **Date Truncation:** All maintenance, fuel, and utilization records were aggregated to the `YYYY-MM` level.

2. **Missing Months:** If a truck had zero utilization and zero maintenance in a given month, a row was generated with `0` for those metrics. This preserves the continuity of the time series.

3. **Maintenance Cost Aggregation:** Summed all `maintenance_records` costs for a given truck-month. If no records existed, the cost is `0` (not null).

4. **Preventive Visit Flag:** Scanned the `maintenance_records` description field for keywords like "PM", "Preventive", or "Routine". Created a binary `had_preventive_visit` flag. 

5. **Downtime Calculation:** Calculated the difference between `shop_out_time` and `shop_in_time` for all maintenance records, then summed by truck-month.

6. **High-Cost Month Definition:** Created a binary `is_high_cost` flag. A month is "high cost" if the total maintenance cost exceeds the 75th percentile of all truck-months (roughly $2,400). This was used as the target variable in the logistic regression.

---

## Anomalies Resolved

- **Negative Downtime:** A small number of records had a `shop_out_time` earlier than the `shop_in_time`. These were corrected to `0` hours (indicating a data entry glitch, not time travel).

- **Fuel vs. Mileage Mismatch:** Some months had fuel purchased but zero miles driven. These were left as-is (trucks can idle), but flagged in the inspection report. 

- **Outliers in Maintenance Cost:** One month had a cost of $45,000 (likely an engine replacement). This was **kept** in the dataset because it is a true high-cost month and the model must learn to predict it, not hide from it.