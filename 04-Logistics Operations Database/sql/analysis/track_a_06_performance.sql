-- ============================================================================
-- Track A | Query A6 — Performance profile of the metric-having population
-- ============================================================================
-- Business question : Among drivers WITH monthly metrics, what does the
--                     performance profile look like, and does it differ
--                     between active and terminated drivers?
-- Why this matters  : Step 3 revealed the 26 leavers have null behavioural
--                     metrics — the model cannot use performance features for
--                     them. This query profiles the metric-having population
--                     (124 active drivers, 0 leavers) so Step 7 knows which
--                     features are usable across the full sample.
-- Expected output   : One row — the overall profile of drivers with metrics.
-- Export target     : sql/analysis/results/track_a_06_performance.csv
-- Tool bounds       : SELECT + aggregate functions + WHERE filter.
-- ============================================================================

SELECT
    COUNT(*)                                AS drivers_with_metrics,
    ROUND(AVG(avg_on_time_rate) * 100, 2)   AS avg_on_time_rate_pct,
    ROUND(MIN(avg_on_time_rate) * 100, 2)   AS min_on_time_rate_pct,
    ROUND(MAX(avg_on_time_rate) * 100, 2)   AS max_on_time_rate_pct,
    ROUND(AVG(avg_mpg), 2)                  AS avg_mpg,
    ROUND(AVG(avg_idle_hours), 2)           AS avg_idle_hours,
    ROUND(AVG(total_miles), 0)              AS avg_total_miles,
    ROUND(AVG(n_low_ontime_months), 1)      AS avg_low_ontime_months
FROM master_driver_clean
WHERE n_months IS NOT NULL;