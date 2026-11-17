-- ============================================================================
-- Track B | Query B4 — Late rate by customer type and freight type
-- ============================================================================
-- Business question : Does late delivery differ by customer type or freight type?
-- Why this matters  : Contract customers often have SLAs with penalties.
--                     Dedicated freight runs on fixed schedules — a late
--                     delivery there is a bigger commercial risk than spot.
-- Expected output   : One row per (customer_type, primary_freight_type).
-- Export target     : sql/analysis/results/track_b_04_by_customer_type.csv
-- Tool bounds       : SELECT + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    customer_type,
    primary_freight_type,
    COUNT(*)                                                AS trips,
    SUM(late_delivery_flag)                                 AS late_trips,
    ROUND(SUM(late_delivery_flag) * 100.0 / COUNT(*), 2)    AS late_rate_pct
FROM master_trip_clean
GROUP BY customer_type, primary_freight_type
HAVING COUNT(*) >= 100
ORDER BY late_rate_pct DESC, trips DESC;