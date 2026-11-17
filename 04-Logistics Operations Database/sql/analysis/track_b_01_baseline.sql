-- ============================================================================
-- Track B | Query B1 — Baseline late rate and monthly trend
-- ============================================================================
-- Business question : What is the overall late rate, and how does it move
--                     month-by-month across 2022-2024?
-- Why this matters  : A stable rate is a systemic scheduling problem. A rising
--                     rate is a deteriorating process. A falling rate is a
--                     working improvement program. The trend tells the
--                     supervisor where the intervention belongs.
-- Expected output   : ~36 rows — one per calendar month — with late counts.
-- Export target     : sql/analysis/results/track_b_01_baseline.csv
-- Tool bounds       : SELECT + SUBSTR (for month extraction) + GROUP BY.
-- ============================================================================

SELECT
    SUBSTR(load_date, 1, 7)                                 AS load_month,
    COUNT(*)                                                AS trips,
    SUM(late_delivery_flag)                                 AS late_trips,
    ROUND(SUM(late_delivery_flag) * 100.0 / COUNT(*), 2)    AS late_rate_pct
FROM master_trip_clean
GROUP BY load_month
ORDER BY load_month;