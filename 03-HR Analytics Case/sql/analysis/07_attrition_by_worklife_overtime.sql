-- ============================================================
-- 07 — Attrition by Work-Life Balance and Average Working Hours
-- ============================================================
-- BUSINESS QUESTION: Does attrition relate to how many hours
--                    employees actually work, and does it
--                    compound with self-reported Work-Life
--                    Balance rating?
-- METRIC:            Attrition rate by WLB band + hours band.
-- GRAIN:             One row per (WLB band, hours band) pair.
-- ============================================================

SELECT
    d.wlb_label                                       AS work_life_balance,
    CASE
        WHEN a.avg_hours < 7.5 THEN '1. Short (<7.5h)'
        WHEN a.avg_hours < 8.0 THEN '2. Normal (7.5-8h)'
        ELSE                        '3. Long (8h+)'
    END                                               AS hours_band,
    COUNT(*)                                          AS total_employees,
    SUM(f.attrition_flag)                             AS leavers,
    ROUND(100.0 * SUM(f.attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM fact_employee f
JOIN attendance_summary a      ON f.employee_id = a.employee_id
JOIN dim_work_life_balance d   ON f.work_life_balance = d.wlb_code
GROUP BY work_life_balance, hours_band
ORDER BY work_life_balance, hours_band;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- Two JOINs in a row:
--   1. fact_employee  -> attendance_summary   (via employee_id)
--   2. fact_employee  -> dim_work_life_balance (via WLB code)
-- Chained JOINs are normal — each one adds data to the
-- combined row.
--
-- CASE WHEN avg_hours ... = bands a continuous number.
--   Same technique as Query 05 (income bands).  Chosen by
--   looking at the actual distribution first:
--     avg_hours range: 5.95 - 11.03, mean 7.70.
--   8h/day is the standard workday, so we split around that.
--
-- IMPORTANT — why we JOIN attendance_summary (inner JOIN, not
-- LEFT JOIN): we want only employees who HAVE attendance data.
-- All 4,410 do (validated in Stage 5), so it's technically
-- equivalent — but semantically we're saying "we require the
-- measurement to exist."  In a dataset with missing attendance
-- this would exclude those employees.
--
-- NULL handling: the JOIN to dim_work_life_balance drops the
-- 38 employees with NULL WLB.  That's consistent with Query 06.
--
-- ORDER BY work_life_balance, hours_band
--   -> sort by WLB first (Bad/Good/Better/Best), then hours
--      within each.  Lets us read the gradient cleanly.
-- ============================================================