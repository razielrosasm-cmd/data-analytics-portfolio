-- ============================================================
-- 08a — Tenure × Hours Overlap Matrix
-- ============================================================
-- BUSINESS QUESTION: Are the "first-year cliff" (34.88% in
--                    0-1 yr) and the "long-hours problem" (26-
--                    45% at 8h+) the SAME people, or two
--                    separate populations?
--                    If worst cell = (0-1 yr × 8h+) and the
--                    rest is quiet -> one population, one
--                    intervention.
--                    If 0-1 yr is high across ALL hours AND
--                    8h+ is high across ALL tenure -> two
--                    populations, two interventions.
-- METRIC:            Attrition rate + gap vs. 16.12%
--                    benchmark, per (tenure × hours) cell.
-- GRAIN:             One row per (tenure band, hours band)
--                    pair -> 15 rows.
-- ============================================================

SELECT
    CASE
        WHEN f.years_at_company <= 1  THEN '1. 0-1 years'
        WHEN f.years_at_company <= 3  THEN '2. 2-3 years'
        WHEN f.years_at_company <= 5  THEN '3. 4-5 years'
        WHEN f.years_at_company <= 10 THEN '4. 6-10 years'
        ELSE                               '5. 10+ years'
    END                                                AS tenure_band,
    CASE
        WHEN a.avg_hours < 7.5 THEN '1. Short (<7.5h)'
        WHEN a.avg_hours < 8.0 THEN '2. Normal (7.5-8h)'
        ELSE                        '3. Long (8h+)'
    END                                                AS hours_band,
    COUNT(*)                                           AS total_employees,
    SUM(f.attrition_flag)                              AS leavers,
    ROUND(100.0 * SUM(f.attrition_flag) / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(
        100.0 * SUM(f.attrition_flag) / COUNT(*) - 16.12
    , 2)                                               AS gap_vs_benchmark_pp
FROM fact_employee f
JOIN attendance_summary a
    ON f.employee_id = a.employee_id
GROUP BY tenure_band, hours_band
ORDER BY tenure_band, hours_band;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- CASE #1 — tenure_band
--   Bands years_at_company into the five locked tenure
--   buckets (0-1 / 2-3 / 4-5 / 6-10 / 10+).
--   I recompute the band here with CASE instead of using the
--   fact_employee.tenure_band column that already exists —
--   keeps the query self-documenting and guarantees the band
--   edges match Section 6 decision #9.
--
--   The '1.', '2.', '3.' prefixes are a sorting trick:
--   because the bands are strings, SQLite would sort
--   '10+ years' before '2-3 years' alphabetically.  Numeric
--   prefixes force the intended order without needing a
--   second CASE block in ORDER BY.
--
-- CASE #2 — hours_band
--   Same idea for avg_hours, matching Query 07's bands:
--   <7.5h / 7.5-8h / 8h+.  Prefix trick again for ordering.
--
-- COUNT(*) AS total_employees
--   Cell size — the denominator for the rate.
--
-- SUM(f.attrition_flag) AS leavers
--   attrition_flag is 0/1, so SUM = count of leavers.
--   Uses the flag column, not the attrition TEXT column,
--   because TEXT ('Yes'/'No') can't be summed.
--
-- ROUND(100.0 * ... / COUNT(*), 2)
--   100.0 not 100 — SQLite integer-division trap (Section 6
--   decision #4).  The 16.12 benchmark is hardcoded per
--   Section 6 decision #1.
--
-- FROM fact_employee f
-- JOIN attendance_summary a ON f.employee_id = a.employee_id
--   INNER JOIN, not LEFT JOIN: we REQUIRE a measured
--   avg_hours to classify the employee into an hours band.
--   Both tables hold exactly 4,410 rows with 0 orphans
--   (validated in Stage 5), so this join is lossless.
--
-- GROUP BY tenure_band, hours_band
--   15 cells = 5 tenure bands × 3 hours bands.
--   SQLite allows grouping by SELECT aliases — no need to
--   repeat the CASE expressions.
--
-- ORDER BY tenure_band, hours_band
--   Strings sort ascending; the '1.'/'2.'/... prefixes give
--   the intended reading order:
--     tenure down the page, hours left-to-right within it.
-- ============================================================