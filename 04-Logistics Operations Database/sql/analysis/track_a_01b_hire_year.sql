-- ============================================================================
-- Track A | Query A1b — Attrition by hire-year cohort
-- ============================================================================
-- Business question : Does attrition differ across hire-year cohorts?
-- Why this matters  : The headline 17.33% hides whether the problem is
--                     structural (uniform across hires) or episodic (one cohort
--                     went badly). The shape of this table determines whether
--                     Step 7's model should include hire_year as a predictor,
--                     and what the executive summary should say about when
--                     turnover started.
-- Expected output   : ~10 rows, one per hire year (2012–2021).
-- Export target     : sql/analysis/results/track_a_01b_hire_year.csv
-- Tool bounds       : Plain SELECT + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    hire_year,
    COUNT(*)                                            AS drivers,
    SUM(driver_attrition)                               AS leavers,
    ROUND(SUM(driver_attrition) * 100.0 / COUNT(*), 2)  AS attrition_rate_pct
FROM master_driver_clean
GROUP BY hire_year
ORDER BY hire_year;