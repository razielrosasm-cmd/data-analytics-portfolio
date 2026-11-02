-- ============================================================
-- 08b — High-Risk Segment Profile (Tenure × Hours)
-- ============================================================
-- BUSINESS QUESTION: Which (tenure × hours) segments carry the
--                    most attrition in absolute terms, and do
--                    they also show elevated self-reported
--                    low Work-Life Balance?
--                    -- 08a proved the two factors COMPOUND,
--                       not overlap.  The year-1 × long-hours
--                       cell is the outlier at 54.42%.
--                    -- 08b filters to cells with a defensible
--                       sample (>= 100 employees) so the short
--                       list is not built on noise.
--                    -- pct_low_wlb tests whether the segment
--                       also *feels* bad, or whether the hours
--                       land regardless of perception.
-- METRIC:            Attrition rate, gap vs. 16.12% benchmark,
--                    and share of the cell rating WLB as
--                    Bad (1) or Good (2).
-- GRAIN:             One row per (tenure band, hours band)
--                    with total_employees >= 100.
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
    , 2)                                               AS gap_vs_benchmark_pp,
    ROUND(
        100.0 * SUM(
            CASE WHEN f.work_life_balance IN (1, 2) THEN 1 ELSE 0 END
        ) / COUNT(*)
    , 2)                                               AS pct_low_wlb
FROM fact_employee f
JOIN attendance_summary a
    ON f.employee_id = a.employee_id
GROUP BY tenure_band, hours_band
HAVING COUNT(*) >= 100
ORDER BY leavers DESC;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- CASE #1 — tenure_band
--   Same five bands as 08a.  Recomputed here (not taken from
--   fact_employee.tenure_band) so the query is self-contained
--   and the band edges stay locked to Section 6 decision #9.
--
-- CASE #2 — hours_band
--   Same three bands as 08a.  Prefix numbers give the intended
--   order without a second CASE block in ORDER BY.
--
-- COUNT(*) AS total_employees
--   Cell size — the denominator.  Also what HAVING filters on.
--
-- SUM(f.attrition_flag) AS leavers
--   attrition_flag is 0/1, so SUM = count of leavers in the
--   cell.  Uses the flag column, not the TEXT 'attrition'
--   column, because TEXT ('Yes'/'No') cannot be summed.
--
-- ROUND(100.0 * SUM(...) / COUNT(*), 2)
--   100.0 not 100 — SQLite integer-division trap (Section 6
--   decision #4).  16.12 benchmark hardcoded per Section 6
--   decision #1.
--
-- pct_low_wlb
--   Percentage of employees in the cell who rated WLB as
--   'Bad' (code 1) or 'Good' (code 2) — the two lowest of the
--   four ratings (Bad / Good / Better / Best).  Computed with
--   a CASE-inside-SUM pattern (conditional aggregation):
--     sum 1 when the condition is true, 0 otherwise, then
--     divide by COUNT(*) to get a share.
--   This is the same technique as a percentage but written
--   inside an aggregate — no new SQL concepts.
--
-- FROM fact_employee f
-- JOIN attendance_summary a ON f.employee_id = a.employee_id
--   INNER JOIN.  Both tables have 4,410 rows, 0 orphans
--   (Stage 5).  Join is lossless.
--
--   We deliberately do NOT join dim_work_life_balance here.
--   The WLB percentage is computed directly from the integer
--   code stored on fact_employee (1=Bad, 2=Good).  Joining
--   the dimension would just be a label lookup and would add
--   no information — the code already encodes the order.
--
-- GROUP BY tenure_band, hours_band
--   15 potential cells (5 × 3).  GROUP BY collapses to one
--   row per cell.
--
-- HAVING COUNT(*) >= 100
--   Drops cells with fewer than 100 employees.
--   HAVING, not WHERE — this is a filter on an AGGREGATE
--   result, not on individual rows.  WHERE runs before GROUP
--   BY and cannot reference COUNT(*).  HAVING runs after.
--   Threshold set at 100 (discussed): 08a showed that even
--   at 100-200 headcount per cell the rates are stable
--   enough to read.  Below 100 we're into small-sample
--   territory (Query 07's Bad × Long cell had n=67 and gave
--   a single-cell 44.78% that is real but fragile).
--
-- ORDER BY leavers DESC
--   Sorts by absolute leaver count, not rate.  Rationale: a
--   report shortlist should be ranked by business impact in
--   people, not by rate — a 3-person cell at 100% is not a
--   business problem.  Rate is still on the row for context.
-- ============================================================