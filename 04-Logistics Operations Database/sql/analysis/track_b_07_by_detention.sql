-- ============================================================================
-- Track B | Query B7 — Late rate by delivery detention band
-- ============================================================================
-- Business question : Do deliveries with high detention (waiting time at the
--                     dock) also run late?
-- Why this matters  : Detention is a symptom of schedule slip at the dock.
--                     High detention + high lateness means dock-side cause.
--                     High detention + low lateness means the dock is
--                     absorbing a transit delay — different fix.
-- Expected output   : 5 rows — one per detention band.
-- Export target     : sql/analysis/results/track_b_07_by_detention.csv
-- Tool bounds       : SELECT + CASE + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    CASE
        WHEN delivery_detention_minutes = 0                  THEN '1. zero'
        WHEN delivery_detention_minutes BETWEEN 1 AND 59     THEN '2. 1-59 min'
        WHEN delivery_detention_minutes BETWEEN 60 AND 119   THEN '3. 60-119 min'
        WHEN delivery_detention_minutes BETWEEN 120 AND 239  THEN '4. 120-239 min'
        ELSE                                                     '5. 240+ min'
    END                                                      AS detention_band,
    COUNT(*)                                                 AS trips,
    SUM(late_delivery_flag)                                  AS late_trips,
    ROUND(SUM(late_delivery_flag) * 100.0 / COUNT(*), 2)     AS late_rate_pct,
    ROUND(AVG(actual_duration_hours), 1)                     AS avg_duration_hours
FROM master_trip_clean
GROUP BY detention_band
ORDER BY detention_band;