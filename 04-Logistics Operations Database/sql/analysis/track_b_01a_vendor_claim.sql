-- ============================================================================
-- Track B | Query B1a — Vendor-claim investigation: three on-time definitions
-- ============================================================================
-- Business question : The Kaggle page claims 85-95% on-time. Our clean table
--                     shows 44.61% on-time (55.39% late). Is this a real
--                     service gap or a definitional artefact?
-- Why this matters  : This is the most important Track B query. It computes
--                     the on-time rate three different ways so we can see
--                     which definition, if any, matches the vendor's claim.
--                     The answer determines the framing of the whole track:
--                     real service problem, definitional mismatch, or both.
-- Expected output   : One row with three independent on-time rate calculations.
-- Export target     : sql/analysis/results/track_b_01a_vendor_claim.csv
-- Tool bounds       : SELECT + CASE + aggregate functions only.
-- ============================================================================

SELECT
    COUNT(*)                                                            AS total_trips,

    -- Definition 1: delivery-only on-time (the target definition we use)
    SUM(delivery_on_time_flag)                                          AS delivery_on_time_count,
    ROUND(SUM(delivery_on_time_flag) * 100.0 / COUNT(*), 2)             AS delivery_on_time_pct,

    -- Definition 2: pickup-only on-time
    SUM(pickup_on_time_flag)                                            AS pickup_on_time_count,
    ROUND(SUM(pickup_on_time_flag) * 100.0 / COUNT(*), 2)               AS pickup_on_time_pct,

    -- Definition 3: both on-time (strictest — counts a trip as on-time
    -- only if pickup AND delivery both met their schedule)
    SUM(CASE
            WHEN pickup_on_time_flag = 1 AND delivery_on_time_flag = 1
            THEN 1 ELSE 0
        END)                                                            AS both_on_time_count,
    ROUND(SUM(CASE
            WHEN pickup_on_time_flag = 1 AND delivery_on_time_flag = 1
            THEN 1 ELSE 0
        END) * 100.0 / COUNT(*), 2)                                     AS both_on_time_pct,

    -- Definition 4: either on-time (loosest — counts a trip as on-time if
    -- pickup OR delivery met schedule)
    SUM(CASE
            WHEN pickup_on_time_flag = 1 OR delivery_on_time_flag = 1
            THEN 1 ELSE 0
        END)                                                            AS either_on_time_count,
    ROUND(SUM(CASE
            WHEN pickup_on_time_flag = 1 OR delivery_on_time_flag = 1
            THEN 1 ELSE 0
        END) * 100.0 / COUNT(*), 2)                                     AS either_on_time_pct

FROM master_trip_clean;