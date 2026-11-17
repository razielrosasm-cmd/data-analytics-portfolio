-- ============================================================================
-- Track A | Query A8 — Static profile: leavers vs active drivers
-- ============================================================================
-- Business question : On static features only, do leavers and active drivers
--                     differ? This decides whether a predictive model can be
--                     built using only non-behavioural features.
-- Why this matters  : Step 3 found that leavers have null behavioural metrics.
--                     If they also look identical to actives on static
--                     features, no predictive model is possible and Track A
--                     must be reframed as descriptive.
-- Expected output   : 2 rows — Active and Terminated — with the same columns.
-- Export target     : sql/analysis/results/track_a_08_no_metrics_puzzle.csv
-- Tool bounds       : SELECT + CASE + GROUP BY.
-- ============================================================================

SELECT
    employment_status,
    COUNT(*)                                              AS drivers,
    ROUND(AVG(age_at_hire), 1)                            AS avg_age_at_hire,
    ROUND(AVG(years_experience), 1)                       AS avg_years_experience,
    ROUND(AVG(hire_year), 0)                              AS avg_hire_year,
    ROUND(AVG(n_incidents), 2)                            AS avg_n_incidents,
    ROUND(AVG(n_at_fault), 2)                             AS avg_n_at_fault,
    ROUND(AVG(total_claim), 0)                            AS avg_total_claim,
    SUM(CASE WHEN cdl_class = 'A' THEN 1 ELSE 0 END)      AS cdl_a_count,
    SUM(CASE WHEN cdl_class = 'B' THEN 1 ELSE 0 END)      AS cdl_b_count
FROM master_driver_clean
GROUP BY employment_status
ORDER BY employment_status;