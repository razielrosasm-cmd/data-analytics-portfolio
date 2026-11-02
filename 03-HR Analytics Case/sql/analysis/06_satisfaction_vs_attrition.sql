-- ============================================================
-- 06 — Satisfaction vs Attrition
-- ============================================================
-- BUSINESS QUESTION: Do employees who report lower job
--                    satisfaction, environment satisfaction, or
--                    work-life balance leave more often?
-- METRIC:            Attrition rate by satisfaction level, for
--                    three satisfaction dimensions in one output.
-- GRAIN:             One row per (dimension, level) pair.
-- ============================================================

SELECT
    'Job Satisfaction'         AS dimension,
    d.job_sat_label            AS level,
    COUNT(*)                   AS total_employees,
    SUM(f.attrition_flag)      AS leavers,
    ROUND(100.0 * SUM(f.attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM fact_employee f
JOIN dim_job_satisfaction d ON f.job_satisfaction = d.job_sat_code
GROUP BY d.job_sat_label

UNION ALL

SELECT
    'Environment Satisfaction' AS dimension,
    d.env_sat_label            AS level,
    COUNT(*)                   AS total_employees,
    SUM(f.attrition_flag)      AS leavers,
    ROUND(100.0 * SUM(f.attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM fact_employee f
JOIN dim_environment_satisfaction d ON f.environment_satisfaction = d.env_sat_code
GROUP BY d.env_sat_label

UNION ALL

SELECT
    'Work-Life Balance'        AS dimension,
    d.wlb_label                AS level,
    COUNT(*)                   AS total_employees,
    SUM(f.attrition_flag)      AS leavers,
    ROUND(100.0 * SUM(f.attrition_flag) / COUNT(*), 2) AS attrition_rate_pct
FROM fact_employee f
JOIN dim_work_life_balance d ON f.work_life_balance = d.wlb_code
GROUP BY d.wlb_label

ORDER BY dimension, attrition_rate_pct DESC;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- This query is THREE queries stitched together with UNION ALL.
--
-- JOIN ... ON ... = connects fact_employee (f) to a dimension
--                   table (d) using the code column.  Replaces
--                   numeric codes (1, 2, 3, 4) with readable
--                   labels ("Low", "Medium", "High", "Very High").
--
-- ALIASES f and d = short names for the tables so you don't have
--                   to retype long table names.  Standard pattern.
--
-- UNION ALL      = stacks the results of 3 SELECTs into one
--                  output.  "ALL" means "keep duplicates" — we
--                  want that, because 'Low' appears in all three
--                  dimensions but they're different rows.
--                  (UNION without ALL would try to dedupe, which
--                  would be wrong here.)
--
-- The three SELECTs are identical in structure — same columns,
-- same order, same data types — which is required for UNION ALL.
-- Only the dimension name, dimension table, and join key change.
--
-- ORDER BY at the END applies to the whole UNION ALL result,
-- not to individual SELECTs.  Sort by dimension first (so each
-- satisfaction dimension is grouped together), then by rate
-- descending within each dimension.
--
-- IMPORTANT — NULL HANDLING:
--   This query uses JOIN (not LEFT JOIN), so employees with
--   NULL satisfaction values (38 WLB, 20 JobSat, 25 EnvSat)
--   are EXCLUDED from this output.  The totals below will not
--   sum to 4,410/711.  That's intentional — we documented in
--   Stage 2 that missingness is informative, and we do NOT
--   impute.  The relevant employees are simply not counted here.
-- ============================================================