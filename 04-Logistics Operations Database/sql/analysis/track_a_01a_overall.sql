-- ============================================================================
-- Track A | Query A1a — Overall driver attrition baseline
-- ============================================================================
-- Business question : What is the overall attrition rate across all 150 drivers?
-- Why this matters  : This is the reference number every other Track A query
--                     is compared against. It also validates that the clean
--                     table matches the Step 3 audit log (26 / 150 = 17.33%).
-- Expected output   : One row, four columns.
-- Export target     : sql/analysis/results/track_a_01a_overall.csv
-- Tool bounds       : Plain SELECT + aggregate functions only.
-- ============================================================================

SELECT
    COUNT(*)                                            AS total_drivers,
    SUM(driver_attrition)                               AS leavers,
    COUNT(*) - SUM(driver_attrition)                    AS active,
    ROUND(SUM(driver_attrition) * 100.0 / COUNT(*), 2)  AS attrition_rate_pct
FROM master_driver_clean;