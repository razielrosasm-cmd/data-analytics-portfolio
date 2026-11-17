-- ============================================================================
-- Track A | Query A9 — Cohort survival: fraction still active by hire year
-- ============================================================================
-- Business question : For each hire year, what fraction of that cohort is
--                     still employed at the company as of end-2024?
-- Why this matters  : This is A1b framed as survival rather than attrition.
--                     It reads more naturally in an executive summary —
--                     "X of the 2015 hires are still with us" is more
--                     intuitive than "the 2015 cohort had 6.67% attrition."
-- Expected output   : ~10 rows, one per hire year, sorted by hire year.
-- Export target     : sql/analysis/results/track_a_09_cohort_survival.csv
-- Tool bounds       : SELECT + CASE + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    hire_year,
    COUNT(*)                                              AS drivers,
    SUM(driver_attrition)                                 AS leavers,
    COUNT(*) - SUM(driver_attrition)                      AS still_active,
    ROUND((COUNT(*) - SUM(driver_attrition)) * 100.0
          / COUNT(*), 2)                                  AS survival_rate_pct
FROM master_driver_clean
GROUP BY hire_year
ORDER BY hire_year;