-- ============================================================
-- 08c2 — Year-7 Spike Check (Unbundling the "4+ years" Band)
-- ============================================================
-- BUSINESS QUESTION: 08c bucketed years_since_last_promotion
--                    into 0 / 1 / 2-3 / 4+ and reported a
--                    37.76% attrition rate for the 4+ band
--                    inside the 6-10 year x Long hours cell.
--                    Is that rate a genuine monotonic
--                    stagnation effect, or an artifact of
--                    the coarse 4+ bucket hiding a single
--                    high-risk raw value?
--                    -- If the rate rises smoothly across
--                       raw values 4,5,6,7,8,9 -> the
--                       stagnation story holds.
--                    -- If one raw value dominates the
--                       band's leaver count -> the finding
--                       is that value, not "stagnation".
-- METRIC:            Attrition rate + headcount, per raw
--                    years_since_last_promotion value.
-- GRAIN:             One row per distinct value of
--                    years_since_last_promotion within the
--                    6-10 year x Long hours cell.
-- ============================================================

SELECT
    f.years_since_last_promotion                       AS years_since_promo,
    COUNT(*)                                           AS total_employees,
    SUM(f.attrition_flag)                              AS leavers,
    ROUND(100.0 * SUM(f.attrition_flag) / COUNT(*), 2) AS attrition_rate_pct,
    ROUND(
        100.0 * SUM(f.attrition_flag) / COUNT(*) - 16.12
    , 2)                                               AS gap_vs_benchmark_pp
FROM fact_employee f
JOIN attendance_summary a
    ON f.employee_id = a.employee_id
WHERE f.years_at_company BETWEEN 6 AND 10
  AND a.avg_hours >= 8.0
GROUP BY f.years_since_last_promotion
ORDER BY f.years_since_last_promotion;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- SELECT f.years_since_last_promotion AS years_since_promo
--   Returns the RAW integer value — not a band.  The whole
--   point of this query is to undo the banding that 08c
--   applied, and check whether the "4+" label was hiding a
--   single high-risk value.
--
-- COUNT(*), SUM(f.attrition_flag), ROUND(...)
--   Same pattern as every prior query.  attrition_flag is
--   0/1 so SUM = leaver count.  100.0 not 100 (Section 6
--   decision #4).  16.12 benchmark hardcoded (Section 6
--   decision #1).
--
-- FROM fact_employee f
-- JOIN attendance_summary a ON f.employee_id = a.employee_id
--   INNER JOIN, same as 08a/b/c.  Lossless.
--
-- WHERE f.years_at_company BETWEEN 6 AND 10
--   AND a.avg_hours >= 8.0
--   Isolates the 6-10 x Long cell — the only cell where 08c
--   showed a monotonic-looking rise across promotion bands.
--   BETWEEN 6 AND 10 is the inclusive lock on the tenure
--   band, matching 08c's WHERE exactly so the totals
--   reconcile (they do: 391 / 94 — same as 08b).
--
-- GROUP BY f.years_since_last_promotion
--   No banding.  One row per raw value in the cell.
--   Expected raw values: 0 through 9 (see distribution
--   below), so ~10 rows.
--
-- ORDER BY f.years_since_last_promotion
--   Sort by raw value ascending so the reader can scan top
--   to bottom and see whether attrition rises smoothly with
--   promotion gap.  A smooth rise = monotonic stagnation
--   story.  A single-value spike = artifact of banding.
-- ============================================================