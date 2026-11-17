-- ============================================================================
-- Track A | Query A5 — Attrition by safety-incident count band
-- ============================================================================
-- Business question : Do drivers with more safety incidents leave at higher rates?
-- Why this matters  : Safety incidents are expensive. If high-incident drivers
--                     leave more, the fleet is being cleaned from within (or by
--                     termination). If low-incident drivers leave more, the
--                     story flips to frustration with safety culture.
-- Expected output   : 4 rows, one per incident-count band.
-- Export target     : sql/analysis/results/track_a_05_by_safety.csv
-- Tool bounds       : SELECT + CASE + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    CASE
        WHEN n_incidents = 0                THEN '0. none'
        WHEN n_incidents = 1                THEN '1. exactly 1'
        WHEN n_incidents BETWEEN 2 AND 3    THEN '2. 2-3'
        ELSE                                     '3. 4+'
    END                                                 AS incidents_band,
    COUNT(*)                                            AS drivers,
    SUM(driver_attrition)                               AS leavers,
    ROUND(SUM(driver_attrition) * 100.0 / COUNT(*), 2)  AS attrition_rate_pct
FROM master_driver_clean
GROUP BY incidents_band
ORDER BY incidents_band;