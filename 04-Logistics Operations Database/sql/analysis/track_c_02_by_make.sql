-- ============================================================================
-- Track C | Query C2 — Average maintenance cost by truck make
-- ============================================================================
-- Business question : Does average maintenance cost differ by truck make?
-- Why this matters  : If one make is systematically cheaper, the supervisor
--                     has a capital-allocation argument for fleet purchases.
--                     If flat, make is not a maintenance lever.
-- Expected output   : One row per make.
-- Export target     : sql/analysis/results/track_c_02_by_make.csv
-- Tool bounds       : SELECT + GROUP BY.
-- ============================================================================

SELECT
    make,
    COUNT(*)                                                AS truck_months,
    COUNT(DISTINCT truck_id)                                AS trucks,
    ROUND(AVG(maintenance_cost), 2)                         AS avg_cost,
    ROUND(AVG(maintenance_events), 2)                       AS avg_events,
    ROUND(AVG(downtime_hours), 1)                           AS avg_downtime_hours,
    ROUND(SUM(high_maintenance_flag) * 100.0 / COUNT(*), 2) AS high_maint_pct
FROM master_truck_month_clean
GROUP BY make
ORDER BY avg_cost DESC;