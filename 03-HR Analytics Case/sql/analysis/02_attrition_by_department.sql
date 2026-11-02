-- ============================================================
-- 02 — Attrition by Department
-- ============================================================
-- BUSINESS QUESTION: Which department is losing employees fastest,
--                    and how far is each department from the
--                    company-wide 16.12% benchmark?
-- METRIC:            Attrition rate, leaver count, dept headcount.
-- GRAIN:             One row per department.
-- ============================================================

SELECT
    department                                        AS department,
    COUNT(*)                                          AS total_employees,
    SUM(attrition_flag)                               AS leavers,
    COUNT(*) - SUM(attrition_flag)                    AS stayers,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2)  AS attrition_rate_pct,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*) - 16.12, 2) AS gap_vs_company_pp
FROM fact_employee
GROUP BY department
ORDER BY attrition_rate_pct DESC;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- department                -> the grouping column: one output row per dept
-- COUNT(*)                  -> how many employees are in that dept
-- SUM(attrition_flag)       -> how many left (0/1 flag summed)
-- COUNT(*) - SUM(...)       -> stayers in that dept
-- 100.0 * SUM(...) / COUNT(*)  -> dept attrition rate as a percentage
--                                (100.0 forces float, not integer math)
-- ROUND(..., 2)             -> 2 decimal places, keeps output readable
-- - 16.12                   -> difference in PERCENTAGE POINTS (pp)
--                                vs the company-wide rate we computed
--                                in query 01.  A dept at 25% shows
--                                +8.88 pp, not "+8.88%".
-- GROUP BY department       -> collapses all 4,410 rows into one row
--                                per unique department
-- ORDER BY ... DESC         -> highest-attrition dept first, so the
--                                business problem is at the top of
--                                the output — recruiters read top-down
--
-- WHY 16.12 IS HARDCODED:
--   For a portfolio, a self-contained query that runs standalone is
--   more valuable than one that requires you to have run a previous
--   query first.  We know the number from Query 01 and it's stable.
--   (In a production BI environment you'd compute it dynamically —
--   that's a FUTURE TOPIC we are deliberately not introducing yet.)
-- ============================================================