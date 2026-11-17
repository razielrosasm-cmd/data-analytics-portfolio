-- ============================================================================
-- Track B | Query B8 — Late rate by trip idle-time band
-- ============================================================================
-- Business question : Do trips with high idle time also run late?
-- Why this matters  : High idle is a proxy for traffic, weather, or waiting
--                     at a customer site. If high-idle trips are also late,
--                     idle is a useful predictor and a driver-facing
--                     recommendation. If not, idle is unrelated to service.
-- Expected output   : 5 rows — one per idle-time band.
-- Export target     : sql/analysis/results/track_b_08_by_idle.csv
-- Tool bounds       : SELECT + CASE + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    CASE
        WHEN idle_time_hours < 2                            THEN '1. under 2 hrs'
        WHEN idle_time_hours BETWEEN 2 AND 4                THEN '2. 2-4 hrs'
        WHEN idle_time_hours BETWEEN 4 AND 7                THEN '3. 4-7 hrs'
        WHEN idle_time_hours BETWEEN 7 AND 11               THEN '4. 7-11 hrs'
        ELSE                                                     '5. 11+ hrs'
    END                                                     AS idle_band,
    COUNT(*)                                                AS trips,
    SUM(late_delivery_flag)                                 AS late_trips,
    ROUND(SUM(late_delivery_flag) * 100.0 / COUNT(*), 2)    AS late_rate_pct,
    ROUND(AVG(actual_distance_miles), 0)                    AS avg_distance_miles
FROM master_trip_clean
GROUP BY idle_band
ORDER BY idle_band;