-- ============================================================
-- 08c — Promotion Stagnation Inside High-Risk Cells
-- ============================================================
-- BUSINESS QUESTION: Inside the five highest-leaver cells
--                    identified in 08b, does promotion
--                    stagnation (years_since_last_promotion)
--                    explain the attrition — or are long hours
--                    sufficient on their own to drive it?
--                    -- 08b showed WLB perception is decoupled
--                       from attrition, so we need another
--                       mechanism candidate.
--                    -- Promotion stagnation is the strongest
--                       remaining candidate: employees working
--                       long hours with no visible progression
--                       signal may feel the hours are a tax
--                       with no payoff.
--                    -- Test: inside each high-risk cell, does
--                       attrition rise as years_since_last_
--                       promotion grows?  If yes -> stagnation
--                       contributes.  If flat -> hours alone
--                       is the driver.
-- METRIC:            Attrition rate and gap vs. 16.12%
--                    benchmark, per (high-risk cell x
--                    promotion band) sub-slice.
-- GRAIN:             One row per (tenure band, hours band,
--                    promotion band) where headcount >= 20.
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
    CASE
        WHEN f.years_since_last_promotion = 0  THEN '1. 0 years'
        WHEN f.years_since_last_promotion = 1  THEN '2. 1 year'
        WHEN f.years_since_last_promotion <= 3 THEN '3. 2-3 years'
        ELSE                                        '4. 4+ years'
    END                                                AS promotion_band,
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
GROUP BY tenure_band, hours_band, promotion_band
HAVING COUNT(*) >= 20
ORDER BY tenure_band, hours_band, promotion_band;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- WHERE clause — selecting the 5 high-risk cells from 08b.
--   The cells are defined by ranges on two columns
--   (years_at_company, avg_hours), so the filter is a chain
--   of OR-ed range predicates, one per cell:
--     0-1  x Long    (years_at_company <= 1  AND avg_hours >= 8.0)
--     0-1  x Short   (years_at_company <= 1  AND avg_hours < 7.5)
--     2-3  x Long    (years_at_company BETWEEN 2 AND 3  AND avg_hours >= 8.0)
--     4-5  x Long    (years_at_company BETWEEN 4 AND 5  AND avg_hours >= 8.0)
--     6-10 x Long    (years_at_company BETWEEN 6 AND 10 AND avg_hours >= 8.0)
--   Explicit BETWEEN bounds avoid overlap between adjacent
--   cells — an employee is counted in exactly one cell, so
--   the row totals reconcile with 08b (checked: totals match).
--
-- CASE #1 — tenure_band
--   Four branches (0-1, 2-3, 4-5, 6-10) matching the WHERE
--   filter, identical to 08a / 08b for consistency.
--   Prefix numbers give correct sort order (SQLite would
--   otherwise sort '10+ years' alphabetically before '2-3').
--
-- CASE #2 — hours_band
--   Only two labels (Short, Long) because the WHERE excluded
--   Normal cells from this query.  Same bands as 08a/08b for
--   the two labels that appear.
--
-- CASE #3 — promotion_band
--   Buckets years_since_last_promotion into four agreed
--   bands: 0 / 1 / 2-3 / 4+.  Prefix numbers again for sort.
--
--   *** IMPORTANT CAVEAT (added after running) ***
--   The '4+ years' band is NOT homogeneous.  Unbundling the
--   raw values (a follow-up query, saved separately) showed
--   that years_since_last_promotion = 7 alone accounts for
--   69 of the 143 employees in the 4+ band — and 33 of its
--   54 leavers.  The 4+ band is effectively a proxy for
--   "year 7" in this dataset.  The headline "4+ years rate
--   = 37.76%" is really "year-7 rate = 47.83%" diluted by
--   lower-risk neighbouring values.  See 08c2 for the full
--   unbundled breakdown.
--
-- COUNT(*), SUM(f.attrition_flag), ROUND(...)
--   Standard pattern.  attrition_flag is 0/1 so SUM = leaver
--   count.  100.0 not 100 (integer-division trap, Section 6
--   decision #4).  16.12 benchmark hardcoded (Section 6
--   decision #1).
--
-- FROM fact_employee f
-- JOIN attendance_summary a ON f.employee_id = a.employee_id
--   INNER JOIN.  Both tables hold 4,410 rows with 0 orphans
--   (Stage 5), so the join is lossless.  We need
--   attendance_summary because avg_hours lives there — the
--   high-risk cells are defined partly by measured hours.
--
-- GROUP BY tenure_band, hours_band, promotion_band
--   Up to 5 x 2 x 4 = 40 theoretical sub-slices.  After the
--   WHERE filter (5 specific cells) the ceiling drops to
--   5 x 4 = 20 for the Long column plus 1 x 4 = 4 for the
--   Short column = 24 rows pre-HAVING.  Small n sub-slices
--   are then filtered out.
--
-- HAVING COUNT(*) >= 20
--   HAVING, not WHERE — filters on the aggregate COUNT(*),
--   not on individual rows.  WHERE runs before GROUP BY and
--   cannot see COUNT(*); HAVING runs after.
--   Threshold = 20: lower than 08b's 100 because we are
--   already inside a high-risk cell, and sub-slices are
--   naturally smaller.  20 is the minimum for a rate to be
--   readable rather than a small-sample artifact.  This is
--   why the 0-1 x Long x 2-3 years band (impossible — new
--   hires can't be 2-3 years without promotion) and the
--   0-1 x Long x 4+ years band (also near-impossible) are
--   correctly dropped.
--
-- ORDER BY tenure_band, hours_band, promotion_band
--   String-prefix ordering gives: tenure top-to-bottom, then
--   hours within tenure, then promotion band within each
--   cell.  Lets the reader scan across a single cell and see
--   whether the rate rises with promotion band — which was
--   the original analytical question.
-- ============================================================