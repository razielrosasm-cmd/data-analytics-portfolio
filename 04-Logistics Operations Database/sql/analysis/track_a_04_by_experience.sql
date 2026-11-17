-- ============================================================================
-- Track A | Query A4 — Attrition by years-of-experience band
-- ============================================================================
-- Business question : Does attrition differ across years-of-experience bands?
-- Why this matters  : If early-career drivers leave more, retention effort
--                     should target the first 12–18 months. If late-career
--                     drivers leave more, the story is retirement or
--                     compensation at the top of the pay scale.
-- Expected output   : 4 rows, one per experience band, sorted by band.
-- Export target     : sql/analysis/results/track_a_04_by_experience.csv
-- Tool bounds       : SELECT + CASE (for banding) + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    CASE
        WHEN years_experience <= 2                THEN '1. 0-2 years'
        WHEN years_experience BETWEEN 3 AND 5     THEN '2. 3-5 years'
        WHEN years_experience BETWEEN 6 AND 10    THEN '3. 6-10 years'
        ELSE                                           '4. 11+ years'
    END                                                 AS experience_band,
    COUNT(*)                                            AS drivers,
    SUM(driver_attrition)                               AS leavers,
    ROUND(SUM(driver_attrition) * 100.0 / COUNT(*), 2)  AS attrition_rate_pct
FROM master_driver_clean
GROUP BY experience_band
ORDER BY experience_band;