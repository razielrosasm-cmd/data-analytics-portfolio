-- ============================================================================
-- Track B | Query B9 — High-risk cell: distance × idle
-- ============================================================================
-- Business question : Where is lateness concentrated in the intersection of
--                     trip distance and trip idle time?
-- Why this matters  : This is the "high-risk cell" cross-tab required by the
--                     master prompt workflow. Step 7's model must beat this
--                     cell or confirm it. The result becomes the operation
--                     "avoid this profile" recommendation.
-- Expected output   : Up to 25 rows — every (distance_band × idle_band)
--                     combination. Some cells will be sparse.
-- Export target     : sql/analysis/results/track_b_09_high_risk_cell.csv
-- Tool bounds       : SELECT + CASE + CASE + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    CASE
        WHEN actual_distance_miles < 500                 THEN '1. under 500 mi'
        WHEN actual_distance_miles BETWEEN 500 AND 1499  THEN '2. 500-1499 mi'
        ELSE                                                  '3. 1500+ mi'
    END                                                  AS distance_band,
    CASE
        WHEN idle_time_hours < 2                         THEN '1. under 2 hrs'
        WHEN idle_time_hours BETWEEN 2 AND 7             THEN '2. 2-7 hrs'
        ELSE                                                  '3. 7+ hrs'
    END                                                  AS idle_band,
    COUNT(*)                                             AS trips,
    SUM(late_delivery_flag)                              AS late_trips,
    ROUND(SUM(late_delivery_flag) * 100.0 / COUNT(*), 2) AS late_rate_pct
FROM master_trip_clean
GROUP BY distance_band, idle_band
ORDER BY distance_band, idle_band;