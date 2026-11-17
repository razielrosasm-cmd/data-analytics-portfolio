-- ============================================================================
-- Track A | Query A1c — Employment status consistency check
-- ============================================================================
-- Business question : Do the two "left the company" signals in the data agree?
-- Why this matters  : The target driver_attrition is derived from
--                     termination_date, but a second field employment_status
--                     also records Active/Terminated. If they disagree, the
--                     target is unreliable and every Track A conclusion is
--                     suspect. This is a data-quality gate, not an analysis.
-- Expected output   : 2 rows — Active and Terminated — with leavers = 0 for
--                     Active and leavers = 26 for Terminated.
-- Export target     : sql/analysis/results/track_a_01c_status_check.csv
-- Tool bounds       : Plain SELECT + GROUP BY.
-- ============================================================================

SELECT
    employment_status,
    COUNT(*)                                            AS drivers,
    SUM(driver_attrition)                               AS leavers
FROM master_driver_clean
GROUP BY employment_status
ORDER BY drivers DESC;