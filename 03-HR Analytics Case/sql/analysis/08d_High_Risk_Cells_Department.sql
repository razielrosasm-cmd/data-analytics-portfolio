-- ============================================================
-- 08d — High-Risk Cells x Department
-- ============================================================
-- BUSINESS QUESTION: Query 02 flagged the Human Resources
--                    department at 30.16% attrition — nearly
--                    2x the company rate.  Query 03 then
--                    flagged the tension that the HR *role*
--                    sits at only 13.46%, so the department
--                    anomaly isn't explained by the role.
--                    08d resolves that "mix effect" by asking:
--                    is the HR department outlier
--                    concentrated inside the specific high-
--                    risk (tenure x hours) cells we found in
--                    08a/08b, or does HR carry elevated
--                    attrition across the board?
--                    -- If HR concentrates inside 0-1 x Long
--                       -> HR has a hiring/onboarding problem
--                          that happens to be worse than other
--                          departments'.
--                    -- If HR is elevated uniformly across cells
--                       -> HR has a department-level cultural
--                          or management problem independent of
--                          tenure/hours.
-- METRIC:            Attrition rate + gap vs. 16.12%
--                    benchmark, per (cell x department)
--                    sub-slice.
-- GRAIN:             One row per (tenure band, hours band,
--                    department) where headcount >= 20.
-- ============================================================

SELECT
    CASE
        WHEN f.years_at_company <= 1  THEN '1. 0-1 years'
        WHEN f.years_at_company <= 3  THEN '2. 2-3 years'
        WHEN f.years_at_company <= 5  THEN '3. 4-5 years'
        WHEN f.years_at_company <= 10 THEN '4. 6-10 years'
    END                                                AS tenure_band,
    CASE
        WHEN a.avg_hours < 7.5 THEN '1. Short (<7.5h)'
        ELSE                        '3. Long (8h+)'
    END                                                AS hours_band,
    f.department                                       AS department,
    COUNT(*)                                           AS total_employees,
    SUM(f.attrition_flag)                              AS leavers,
    ROUND(100.0 * SUM(f.attrition_flag) / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(
        100.0 * SUM(f.attrition_flag) / COUNT(*) - 16.12
    , 2)                                               AS gap_vs_benchmark_pp
FROM fact_employee f
JOIN attendance_summary a
    ON f.employee_id = a.employee_id
WHERE (
        (f.years_at_company <= 1  AND a.avg_hours >= 8.0)
     OR (f.years_at_company <= 1  AND a.avg_hours < 7.5)
     OR (f.years_at_company BETWEEN 2  AND 3  AND a.avg_hours >= 8.0)
     OR (f.years_at_company BETWEEN 4  AND 5  AND a.avg_hours >= 8.0)
     OR (f.years_at_company BETWEEN 6  AND 10 AND a.avg_hours >= 8.0)
      )
GROUP BY tenure_band, hours_band, department
HAVING COUNT(*) >= 20
ORDER BY tenure_band, hours_band, leavers DESC;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- WHERE clause — IDENTICAL to 08c.  Same five high-risk cells
--   from 08b, same BETWEEN boundaries.  Deliberately kept
--   identical so 08c and 08d are directly comparable — any
--   difference in row counts between the two queries is
--   *only* due to the grouping axis change (promotion_band
--   vs. department), never due to a filter difference.
--
-- CASE #1 — tenure_band
--   Four branches (0-1, 2-3, 4-5, 6-10).  Same as 08a/b/c.
--   Prefix numbers for correct sort order.
--
-- CASE #2 — hours_band
--   Short / Long only (Normal excluded by WHERE).
--
-- f.department
--   Raw text column.  Values expected: 'Human Resources',
--   'Research & Development', 'Sales'.  No CASE needed —
--   the labels are already clean, and there are only three
--   of them.
--
-- COUNT(*), SUM(f.attrition_flag), ROUND(...)
--   Same pattern.  attrition_flag is 0/1.  100.0 not 100
--   (Section 6 decision #4).  16.12 benchmark hardcoded
--   (Section 6 decision #1).
--
-- FROM fact_employee f
-- JOIN attendance_summary a ON f.employee_id = a.employee_id
--   INNER JOIN, lossless (both 4,410 rows, 0 orphans).
--
-- GROUP BY tenure_band, hours_band, department
--   Up to 5 cells x 3 departments = 15 potential rows.
--   After HAVING filter, expect ~10-13 rows (HR has only
--   189 total employees, so HR slices inside narrow cells
--   will often fall below the 20-row threshold and drop).
--
--   NOTE — this is why HR slices will be sparse.  HR is
--   4.3% of headcount (189 / 4410).  Inside a cell like
--   "6-10 x Long" (391 employees total), you'd expect only
--   ~17 HR employees on average — below the HAVING >= 20
--   threshold.  So HR will likely only appear in cells
--   where it's genuinely over-represented.  That's actually
--   a feature, not a bug: absence of HR in the output is
--   itself information (HR is *not* over-concentrated in
--   that cell).
--
-- HAVING COUNT(*) >= 20
--   HAVING, not WHERE — filters on the aggregate.  Same
--   threshold as 08c for consistency.  Drops sub-slices
--   too small to read reliably.  Row loss to this filter
--   is expected and correct.
--
-- ORDER BY tenure_band, hours_band, leavers DESC
--   Sorts by cell first (tenure, then hours), then within
--   each cell orders departments by absolute leaver count
--   descending.  This puts the biggest contributor inside
--   each cell at the top, which is exactly what we need to
--   answer "is HR the driver here, or is it R&D/Sales?"
--   inside any given cell.
-- ============================================================