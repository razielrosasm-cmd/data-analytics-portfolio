-- ============================================================
-- 03 — Attrition by Job Role
-- ============================================================
-- BUSINESS QUESTION: Which specific job roles drive attrition,
--                    and does role-level detail explain the
--                    HR department outlier we saw in Query 02?
-- METRIC:            Attrition rate, leaver count, role headcount.
-- GRAIN:             One row per job role.
-- ============================================================

SELECT
    job_role                                          AS job_role,
    COUNT(*)                                          AS total_employees,
    SUM(attrition_flag)                               AS leavers,
    COUNT(*) - SUM(attrition_flag)                    AS stayers,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2)  AS attrition_rate_pct,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*) - 16.12, 2) AS gap_vs_company_pp
FROM fact_employee
GROUP BY job_role
ORDER BY attrition_rate_pct DESC;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- Same structure as Query 02, but grouped by job_role instead of
-- department.  A job role is a finer grain than a department, so
-- we expect more rows and more variation.
--
-- KEY POINT — WHY SEGMENT FINER:
--   A department-level average can hide two roles going in
--   opposite directions (e.g. one role at 40%, another at 5%,
--   averaging to 22%).  Query 03 checks whether the HR dept
--   finding is a "whole-department" problem or a "specific role"
--   problem — the fix is completely different in each case.
--
-- REMINDER ON 100.0 AND 16.12:
--   Same as Queries 01 and 02.  100.0 forces float division.
--   16.12 is the locked-in company benchmark from Query 01.
-- ============================================================