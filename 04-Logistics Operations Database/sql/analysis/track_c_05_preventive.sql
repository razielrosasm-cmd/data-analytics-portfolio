-- ============================================================================
-- Track C | Query C5 — Preventive maintenance and total cost
-- ============================================================================
-- Business question : Do months with more preventive maintenance records
--                     have lower total maintenance cost?
-- Why this matters  : This is the classic prevention argument. If preventive
--                     work reduces total cost, the supervisor should tighten
--                     PM cadence. If it does not, prevention is not paying
--                     for itself in this fleet.
-- Expected output   : 4 rows — one per preventive count band.
-- Export target     : sql/analysis/results/track_c_05_preventive.csv
-- Tool bounds       : SELECT + CASE + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    CASE
        WHEN n_preventive = 0                           THEN '1. none'
        WHEN n_preventive = 1                           THEN '2. one'
        WHEN n_preventive BETWEEN 2 AND 3               THEN '3. two-three'
        ELSE                                                 '4. four+'
    END                                                 AS preventive_band,
    COUNT(*)                                            AS truck_months,
    ROUND(AVG(maintenance_cost), 2)                     AS avg_cost,
    ROUND(AVG(maintenance_events), 2)                   AS avg_total_events,
    ROUND(AVG(downtime_hours), 1)                       AS avg_downtime_hours,
    ROUND(SUM(high_maintenance_flag) * 100.0 / COUNT(*), 2) AS high_maint_pct
FROM master_truck_month_clean
GROUP BY preventive_band
ORDER BY preventive_band;