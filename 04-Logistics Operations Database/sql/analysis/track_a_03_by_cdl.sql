-- ============================================================================
-- Track A | Query A3 — Attrition by CDL class and employment status
-- ============================================================================
-- Business question : Does attrition differ across CDL classes (A/B)?
-- Why this matters  : CDL class defines the labour market each driver belongs
--                     to. If one class dominates the attrition, retention
--                     efforts should not be uniform across the fleet.
-- Expected output   : One row per (cdl_class, employment_status) combination.
-- Export target     : sql/analysis/results/track_a_03_by_cdl.csv
-- Tool bounds       : SELECT + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    cdl_class,
    employment_status,
    COUNT(*)                                            AS drivers,
    SUM(driver_attrition)                               AS leavers,
    ROUND(SUM(driver_attrition) * 100.0 / COUNT(*), 2)  AS attrition_rate_pct
FROM master_driver_clean
GROUP BY cdl_class, employment_status
ORDER BY cdl_class, attrition_rate_pct DESC;