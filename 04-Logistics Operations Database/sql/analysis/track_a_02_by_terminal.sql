-- ============================================================================
-- Track A | Query A2 — Attrition by home terminal
-- ============================================================================
-- Business question : Does driver attrition differ across home terminals?
-- Why this matters  : A single high-attrition terminal turns the story from
--                     "structural turnover" into "local problem" — different
--                     recommendation, different cost. If attrition is uniform,
--                     the fix is policy; if it is concentrated, the fix is
--                     managerial.
-- Expected output   : One row per terminal, sorted by attrition rate descending.
-- Export target     : sql/analysis/results/track_a_02_by_terminal.csv
-- Tool bounds       : SELECT + GROUP BY + HAVING (drivers >= 3) + ORDER BY.
-- ============================================================================

SELECT
    home_terminal,
    COUNT(*)                                            AS drivers,
    SUM(driver_attrition)                               AS leavers,
    ROUND(SUM(driver_attrition) * 100.0 / COUNT(*), 2)  AS attrition_rate_pct
FROM master_driver_clean
GROUP BY home_terminal
HAVING COUNT(*) >= 3
ORDER BY attrition_rate_pct DESC, drivers DESC;