-- ============================================================================
-- Track B | Query B3 — Worst routes by late rate
-- ============================================================================
-- Business question : Which routes are worst by late rate, restricted to
--                     routes with enough volume to be statistically meaningful?
-- Why this matters  : If a small set of routes carries a disproportionate
--                     share of late deliveries, the supervisor's fix is
--                     targeted. If all routes are similar, the fix is systemic.
-- Expected output   : One row per route, sorted by late rate descending.
-- Export target     : sql/analysis/results/track_b_03_by_route.csv
-- Tool bounds       : SELECT + GROUP BY + HAVING + ORDER BY.
-- ============================================================================

SELECT
    origin_city || ' -> ' || destination_city                  AS route,
    COUNT(*)                                                   AS trips,
    SUM(late_delivery_flag)                                    AS late_trips,
    ROUND(SUM(late_delivery_flag) * 100.0 / COUNT(*), 2)       AS late_rate_pct,
    ROUND(AVG(actual_distance_miles), 0)                       AS avg_distance_miles,
    ROUND(AVG(typical_transit_days), 1)                        AS typical_transit_days
FROM master_trip_clean
GROUP BY origin_city, destination_city
HAVING COUNT(*) >= 200
ORDER BY late_rate_pct DESC, trips DESC;