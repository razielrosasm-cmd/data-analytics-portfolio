-- ============================================================================
-- Track C | Query C6 — Cost and downtime relationship
-- ============================================================================
-- Business question : Do months with high maintenance cost also have high
--                     downtime?
-- Why this matters  : Downtime is the hidden cost of maintenance. If cost
--                     and downtime move together, the supervisor's real
--                     maintenance cost is higher than invoices show. If
--                     they are decoupled, some expensive repairs are fast
--                     and some cheap repairs are slow — different lever.
-- Expected output   : 4 rows — one per downtime band.
-- Export target     : sql/analysis/results/track_c_06_downtime.csv
-- Tool bounds       : SELECT + CASE + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    CASE
        WHEN downtime_hours = 0                             THEN '1. zero'
        WHEN downtime_hours BETWEEN 1 AND 23                THEN '2. 1-23 hrs'
        WHEN downtime_hours BETWEEN 24 AND 71               THEN '3. 24-71 hrs'
        ELSE                                                     '4. 72+ hrs'
    END                                                     AS downtime_band,
    COUNT(*)                                                AS truck_months,
    ROUND(AVG(maintenance_cost), 2)                         AS avg_cost,
    ROUND(AVG(maintenance_events), 2)                       AS avg_events,
    ROUND(SUM(high_maintenance_flag) * 100.0 / COUNT(*), 2) AS high_maint_pct
FROM master_truck_month_clean
GROUP BY downtime_band
ORDER BY downtime_band;