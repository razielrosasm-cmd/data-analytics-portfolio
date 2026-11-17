-- ============================================================================
-- Track A | Query A7 — High-risk cell: experience × incidents
-- ============================================================================
-- Business question : Where is attrition concentrated in the intersection of
--                     experience and safety-incident count?
-- Why this matters  : This is the "high-risk cell" referenced in the master
--                     prompt workflow — a two-dimensional cross-tab that
--                     identifies the operational segment where turnover is
--                     worst. Step 7's model must either confirm this cell or
--                     discover a better one.
-- Expected output   : 16 rows — every (experience_band × incidents_band)
--                     combination, including combinations with zero drivers.
-- Export target     : sql/analysis/results/track_a_07_high_risk_cell.csv
-- Tool bounds       : SELECT + CASE + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    CASE
        WHEN years_experience <= 2             THEN '1. 0-2 years'
        WHEN years_experience BETWEEN 3 AND 5  THEN '2. 3-5 years'
        WHEN years_experience BETWEEN 6 AND 10 THEN '3. 6-10 years'
        ELSE                                        '4. 11+ years'
    END                                                 AS experience_band,
    CASE
        WHEN n_incidents = 0                   THEN '0. no incidents'
        WHEN n_incidents = 1                   THEN '1. one incident'
        ELSE                                        '2. two or more'
    END                                                 AS incidents_band,
    COUNT(*)                                            AS drivers,
    SUM(driver_attrition)                               AS leavers,
    ROUND(SUM(driver_attrition) * 100.0 / COUNT(*), 2)  AS attrition_rate_pct
FROM master_driver_clean
GROUP BY experience_band, incidents_band
ORDER BY experience_band, incidents_band;