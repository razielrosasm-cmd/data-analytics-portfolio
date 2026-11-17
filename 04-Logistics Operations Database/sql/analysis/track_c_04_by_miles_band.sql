-- ============================================================================
-- Track C | Query C4 — Maintenance cost by monthly mileage band
-- ============================================================================
-- Business question : Does maintenance cost rise with monthly mileage?
-- Why this matters  : Heavy-use trucks should have more maintenance. If cost
--                     tracks miles, the supervisor can forecast maintenance
--                     from utilization — a real operational lever. If flat,
--                     the relationship between use and cost is absent.
-- Expected output   : 5 rows — one per mileage band.
-- Export target     : sql/analysis/results/track_c_04_by_miles_band.csv
-- Tool bounds       : SELECT + CASE + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    CASE
        WHEN total_miles < 5000                             THEN '1. under 5k'
        WHEN total_miles BETWEEN 5000 AND 9999              THEN '2. 5-10k'
        WHEN total_miles BETWEEN 10000 AND 14999            THEN '3. 10-15k'
        WHEN total_miles BETWEEN 15000 AND 19999            THEN '4. 15-20k'
        ELSE                                                     '5. 20k+'
    END                                                     AS miles_band,
    COUNT(*)                                                AS truck_months,
    ROUND(AVG(maintenance_cost), 2)                         AS avg_cost,
    ROUND(AVG(maintenance_events), 2)                       AS avg_events,
    ROUND(AVG(downtime_hours), 1)                           AS avg_downtime_hours,
    ROUND(SUM(high_maintenance_flag) * 100.0 / COUNT(*), 2) AS high_maint_pct
FROM master_truck_month_clean
GROUP BY miles_band
ORDER BY miles_band;