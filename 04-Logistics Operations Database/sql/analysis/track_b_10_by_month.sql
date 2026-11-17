-- ============================================================================
-- Track B | Query B10 — Late rate by calendar month (seasonality)
-- ============================================================================
-- Business question : Does late rate show a seasonal pattern across calendar
--                     months, aggregated over 2022-2024?
-- Why this matters  : Seasonality affects capacity planning. If Q4 is worse,
--                     the supervisor plans extra capacity in advance. If flat,
--                     capacity planning is not the lever.
-- Expected output   : 12 rows — one per calendar month (Jan-Dec), aggregated.
-- Export target     : sql/analysis/results/track_b_10_by_month.csv
-- Tool bounds       : SELECT + SUBSTR (for month extraction) + GROUP BY.
-- ============================================================================

SELECT
    SUBSTR(load_date, 6, 2)                                 AS calendar_month,
    COUNT(*)                                                AS trips,
    SUM(late_delivery_flag)                                 AS late_trips,
    ROUND(SUM(late_delivery_flag) * 100.0 / COUNT(*), 2)    AS late_rate_pct
FROM master_trip_clean
GROUP BY calendar_month
ORDER BY calendar_month;