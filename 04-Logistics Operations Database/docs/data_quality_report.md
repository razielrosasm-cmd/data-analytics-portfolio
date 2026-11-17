# Data Quality Report — Logistics Operations Database

This report summarizes the findings from the initial data inspection phase (`python/analysis/01_inspect.py`). The purpose is to validate the raw source files and document any data quality issues before cleaning and analysis.

**Source Data:** 16 raw CSV files in `data/raw/`
**Total Records Analyzed:** ~120,000 rows across all tables

---

## Overall Data Health

The raw data is structurally sound. Primary keys are unique, foreign keys resolve correctly, and the overall missing-value rate is low. No entire tables or columns were missing. However, there are a few operational quirks that required specific handling during the cleaning phase.

---

## Table-by-Table Findings

### Drivers (`drivers.csv`)
- **Total Rows:** 450
- **Issues:** 
  - 0% missing `driver_id` (primary key is solid).
  - 26 drivers have a populated `termination_date`. These are the 26 leavers identified in Track A.
  - `cdl_class` has 2% missing values (9 drivers). These were left as null, as it does not affect the analysis.

### Trips (`trips.csv`)
- **Total Rows:** 84,500
- **Issues:**
  - `actual_distance_miles` was stored as **Text** in the raw CSV (e.g., "1,200"). It had to be converted to a numeric format during the Python cleaning phase.
  - `scheduled_delivery` and `actual_delivery` timestamps had 0% missing values, allowing a 100% accurate calculation of the late-delivery flag.

### Maintenance Records (`maintenance_records.csv`)
- **Total Rows:** 2,850
- **Issues:**
  - `cost` has 0% missing values.
  - `shop_in_time` and `shop_out_time` contain a few instances of negative duration (e.g., shop out time is before shop in time). These were flagged and corrected to 0 hours during cleaning.
  - **Key Finding:** About 60% of these records contain the word "Preventive" or "PM" in the description. This is what defined the `had_preventive_visit` flag.

### Truck Utilization (`truck_utilization_metrics.csv`)
- **Total Rows:** 3,600 (representing 100 trucks over 36 months)
- **Issues:**
  - This table defines the core `truck_month` grain. 
  - 288 rows (8%) had `miles_driven` as null. During cleaning, these were imputed to `0` if the truck was marked as inactive, or calculated from route data if active.

### Delivery Events (`delivery_events.csv`)
- **Total Rows:** ~15,000
- **Issues:**
  - 15% of events had missing timestamps for `event_time`. 
  - These were investigated and determined to be system sync glitches. They were excluded from the detention/idle time calculations, as they could not be accurately timed.

---

## Referential Integrity Check

A rigorous check was run to ensure all foreign keys mapped correctly:

- ✅ All `trip.driver_id` values exist in `drivers.driver_id`.
- ✅ All `trip.truck_id` values exist in `trucks.truck_id`.
- ✅ All `maintenance.truck_id` values exist in `trucks.truck_id`.
- ✅ All `trip.route_id` values exist in `routes.route_id`.

No orphaned records were found.

---

## Conclusion

The data quality is sufficient for the planned analysis. The main cleaning hurdle was the text-to-numeric conversion of the distance field, which was successfully resolved. The high integrity of the maintenance and trip tables gives strong confidence in the Track B and Track C findings.