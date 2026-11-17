-- ============================================================================
-- Track B | Query B6 — Late rate by distance band
-- ============================================================================
-- Business question : Does late delivery rise with trip distance?
-- Why this matters  : Long-haul accumulates more risk. If the late rate is
--                     flat across distance bands, lateness is a scheduling
--                     artefact. If it rises, distance belongs in the model.
-- Expected output   : 5 rows — one per distance band.
-- Export target     : sql/analysis/results/track_b_06_by_distance_band.csv
-- Tool bounds       : SELECT + CASE + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    CASE
        WHEN actual_distance_miles < 500                    THEN '1. under 500 mi'
        WHEN actual_distance_miles BETWEEN 500 AND 999      THEN '2. 500-999 mi'
        WHEN actual_distance_miles BETWEEN 1000 AND 1499    THEN '3. 1000-1499 mi'
        WHEN actual_distance_miles BETWEEN 1500 AND 1999    THEN '4. 1500-1999 mi'
        ELSE                                                     '5. 2000+ mi'
    END                                                     AS distance_band,
    COUNT(*)                                                AS trips,
    SUM(late_delivery_flag)                                 AS late_trips,
    ROUND(SUM(late_delivery_flag) * 100.0 / COUNT(*), 2)    AS late_rate_pct
FROM master_trip_clean
GROUP BY distance_band
ORDER BY distance_band;