-- ============================================================================
-- Track C | Query C3 — Maintenance cost by truck age band
-- ============================================================================
-- Business question : Does maintenance cost rise with truck age?
-- Why this matters  : The textbook expectation is yes. If the pattern holds
--                     here, it is a strong signal for fleet renewal decisions
--                     and gives the supervisor a real recommendation. If it
--                     does NOT hold, the data confirms that maintenance cost
--                     is also random.
-- Expected output   : 5 rows — one per truck age band.
-- Export target     : sql/analysis/results/track_c_03_by_age_band.csv
-- Tool bounds       : SELECT + CASE + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    CASE
        WHEN truck_age_years < 3                            THEN '1. 0-2.9 yrs'
        WHEN truck_age_years BETWEEN 3 AND 4.99             THEN '2. 3-4.9 yrs'
        WHEN truck_age_years BETWEEN 5 AND 6.99             THEN '3. 5-6.9 yrs'
        WHEN truck_age_years BETWEEN 7 AND 8.99             THEN '4. 7-8.9 yrs'
        ELSE                                                     '5. 9+ yrs'
    END                                                     AS age_band,
    COUNT(*)                                                AS truck_months,
    COUNT(DISTINCT truck_id)                                AS trucks,
    ROUND(AVG(maintenance_cost), 2)                         AS avg_cost,
    ROUND(AVG(maintenance_events), 2)                       AS avg_events,
    ROUND(AVG(downtime_hours), 1)                           AS avg_downtime_hours,
    ROUND(SUM(high_maintenance_flag) * 100.0 / COUNT(*), 2) AS high_maint_pct
FROM master_truck_month_clean
GROUP BY age_band
ORDER BY age_band;