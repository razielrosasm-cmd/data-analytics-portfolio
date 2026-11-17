-- ============================================================================
-- Track C | Query C1 — Baseline cost distribution
-- ============================================================================
-- Business question : What does the maintenance_cost distribution look like
--                     across all 3,312 truck-months?
-- Why this matters  : A wide distribution means a few truck-months dominate
--                     spend — that is where the supervisor should focus.
--                     A narrow distribution means maintenance cost is uniform
--                     and the lever is fleet-wide (PM cadence, parts
--                     contracts) not per-truck.
-- Expected output   : One row with distribution summary statistics.
-- Export target     : sql/analysis/results/track_c_01_baseline.csv
-- Tool bounds       : SELECT + aggregate functions + scalar subquery-free
--                     percentile approximation via AVG and CASE.
-- ============================================================================

SELECT
    COUNT(*)                                                AS truck_months,
    ROUND(AVG(maintenance_cost), 2)                         AS avg_cost,
    ROUND(MIN(maintenance_cost), 2)                         AS min_cost,
    ROUND(MAX(maintenance_cost), 2)                         AS max_cost,
    SUM(high_maintenance_flag)                              AS high_maint_months,
    ROUND(SUM(high_maintenance_flag) * 100.0 / COUNT(*), 2) AS high_maint_pct,
    ROUND(SUM(maintenance_cost), 2)                         AS total_spend,
    ROUND(AVG(CASE WHEN high_maintenance_flag = 1
                   THEN maintenance_cost END), 2)           AS avg_cost_high_months,
    ROUND(SUM(CASE WHEN high_maintenance_flag = 1
                   THEN maintenance_cost ELSE 0 END) * 100.0
          / SUM(maintenance_cost), 2)                       AS pct_spend_from_high_months
FROM master_truck_month_clean;