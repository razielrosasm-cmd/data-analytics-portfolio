-- ============================================================
-- 08d2 — R&D x Year-1 x Long Hours: Role Breakdown
-- ============================================================
-- BUSINESS QUESTION: 08d identified the single biggest
--                    attrition contributor in Stage 6:
--                    R&D x 0-1 yr x Long hours = 135
--                    employees, 77 leavers, 57.04% rate.
--                    That one cell is 10.8% of all company
--                    attrition from 3.1% of headcount.
--                    But "R&D" is a department, not an
--                    intervention target.  Which job roles
--                    inside R&D are producing this cell?
--                    -- If the 77 leavers concentrate in one
--                       or two roles -> targeted fix (recruit
--                       differently, onboard differently for
--                       that role).
--                    -- If spread evenly across roles -> it's a
--                       department-level or team-level problem,
--                       not a role-level one, and intervention
--                       belongs to R&D leadership, not to
--                       recruiting.
-- METRIC:            Attrition rate + gap vs. 16.12%
--                    benchmark, per job_role inside the
--                    R&D x 0-1 x Long cell.
-- GRAIN:             One row per job_role where headcount >= 10.
-- NOTE:              Some employees have department =
--                    'Research & Development' while job_role =
--                    'Sales Executive' / 'Sales Representative'
--                    / 'Manager' / 'Human Resources'.  This is
--                    a real feature of the source dataset, not
--                    a data-quality bug (Section 6 decision
--                    #14).  All findings are department-based,
--                    so the artifact does not affect
--                    conclusions.
-- ============================================================

SELECT
    f.job_role                                         AS job_role,
    COUNT(*)                                           AS total_employees,
    SUM(f.attrition_flag)                              AS leavers,
    ROUND(100.0 * SUM(f.attrition_flag) / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(
        100.0 * SUM(f.attrition_flag) / COUNT(*) - 16.12
    , 2)                                               AS gap_vs_benchmark_pp
FROM fact_employee f
JOIN attendance_summary a
    ON f.employee_id = a.employee_id
WHERE f.years_at_company <= 1
  AND a.avg_hours >= 8.0
  AND f.department = 'Research & Development'
GROUP BY f.job_role
HAVING COUNT(*) >= 10
ORDER BY leavers DESC;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- SELECT f.job_role
--   The grouping axis for this query.  job_role is a text
--   column on fact_employee with 9 distinct values in the full
--   dataset (Research Director, Research Scientist, Laboratory
--   Technician, Sales Executive, Sales Representative, Manager,
--   Human Resources, Manufacturing Director, Healthcare
--   Representative).  Inside this single cell (R&D x 0-1 x
--   Long) most roles appear, but at very different sizes.
--
-- COUNT(*), SUM(f.attrition_flag), ROUND(...)
--   Standard pattern.  attrition_flag is 0/1 so SUM = leaver
--   count.  100.0 not 100 (integer-division trap, Section 6
--   decision #4).  16.12 benchmark hardcoded (Section 6
--   decision #1).
--
-- FROM fact_employee f
-- JOIN attendance_summary a ON f.employee_id = a.employee_id
--   INNER JOIN, lossless (both 4,410 rows, 0 orphans per
--   Stage 5 validation).  Needed because avg_hours lives on
--   attendance_summary.
--
-- WHERE f.years_at_company <= 1
--   AND a.avg_hours >= 8.0
--   AND f.department = 'Research & Development'
--   Three predicates define the exact cell:
--     - tenure: year 1 (matches the '0-1 years' band from
--       08a/08b/08c/08d)
--     - hours: Long (>= 8.0, matches the 'Long (8h+)' band)
--     - department: R&D (the largest single contributor)
--   No CASE needed here — the cell is a fixed point, not a
--   range, so the WHERE is written directly instead of with
--   an OR-ed chain of range predicates (compare 08c/08d's
--   WHERE clause, which had to encode 5 separate cells).
--
-- GROUP BY f.job_role
--   Collapses rows into one per distinct role inside the
--   cell.  Without the HAVING filter this would return 9
--   rows; with HAVING >= 10 it returns 4 rows covering
--   96 of 135 employees (71% of the cell).
--
-- HAVING COUNT(*) >= 10
--   HAVING, not WHERE — filters on the aggregate COUNT(*).
--   Threshold = 10 (lower than 08c/08d's 20) because we are
--   inside a single 135-person cell and role slices are
--   naturally small.  10 is the minimum for a rate to be
--   readable rather than a single-employee fluke.  Roles
--   below 10 (Sales Representative n=9, Research Director
--   n=9, Manager n=9, Human Resources n=9, Healthcare
--   Representative n=3) are dropped here — but note they
--   still exist and are captured in the no-HAVING companion
--   run, which confirms the role-uniform pattern (all at
--   33-67% attrition).
--
-- ORDER BY leavers DESC
--   Sorts by absolute leaver count, not rate.  Rationale:
--   the question is "which roles are producing the 77
--   leavers?" — an absolute-count ranking answers that
--   directly.  Rate is still shown for context.  (Consistent
--   with 08b's rationale.)
-- ============================================================