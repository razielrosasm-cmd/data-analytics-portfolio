-- ============================================================================
-- Track B | Query B2 — Pickup vs delivery lateness comparison
-- ============================================================================
-- Business question : Is pickup lateness distributed the same as delivery
--                     lateness?
-- Why this matters  : If pickup is punctual but delivery is late, the delay
--                     happens in transit. If both are late, the problem is
--                     at the dock. Two different operational fixes.
-- Expected output   : 2 rows — Pickup and Delivery — same columns.
-- Export target     : sql/analysis/results/track_b_02_pickup_vs_delivery.csv
-- Tool bounds       : SELECT + UNION ALL + aggregate functions.
-- ============================================================================

SELECT
    'Pickup'                                                AS event_type,
    COUNT(*)                                                AS events,
    SUM(pickup_late_flag)                                   AS late_events,
    ROUND(SUM(pickup_late_flag) * 100.0 / COUNT(*), 2)      AS late_rate_pct,
    ROUND(AVG(pickup_detention_minutes), 1)                 AS avg_detention_minutes
FROM master_trip_clean
WHERE pickup_on_time_flag IS NOT NULL

UNION ALL

SELECT
    'Delivery'                                              AS event_type,
    COUNT(*)                                                AS events,
    SUM(late_delivery_flag)                                 AS late_events,
    ROUND(SUM(late_delivery_flag) * 100.0 / COUNT(*), 2)    AS late_rate_pct,
    ROUND(AVG(delivery_detention_minutes), 1)               AS avg_detention_minutes
FROM master_trip_clean
WHERE delivery_on_time_flag IS NOT NULL;