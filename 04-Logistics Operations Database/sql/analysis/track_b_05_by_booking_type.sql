-- ============================================================================
-- Track B | Query B5 — Late rate by booking type (Spot vs Dedicated)
-- ============================================================================
-- Business question : Do Spot loads run later than Dedicated loads?
-- Why this matters  : Spot freight is bought on demand with less planning;
--                     Dedicated runs on fixed schedules. If Spot is
--                     significantly worse, the story is a capacity allocation
--                     problem, and the fix is to reserve capacity for
--                     committed freight.
-- Expected output   : 2 rows — Spot and Dedicated — same columns.
-- Export target     : sql/analysis/results/track_b_05_by_booking_type.csv
-- Tool bounds       : SELECT + GROUP BY.
-- ============================================================================

SELECT
    booking_type,
    COUNT(*)                                                AS trips,
    SUM(late_delivery_flag)                                 AS late_trips,
    ROUND(SUM(late_delivery_flag) * 100.0 / COUNT(*), 2)    AS late_rate_pct,
    ROUND(AVG(actual_distance_miles), 0)                    AS avg_distance_miles
FROM master_trip_clean
GROUP BY booking_type
ORDER BY late_rate_pct DESC;