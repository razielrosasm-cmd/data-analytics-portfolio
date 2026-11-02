-- ============================================================
-- 04 — Attrition by Tenure Band
-- ============================================================
-- BUSINESS QUESTION: When in an employee's lifecycle does
--                    attrition happen?  Are we losing people
--                    in their first year, at year 5, or at 10+?
-- METRIC:            Attrition rate by tenure band.
-- GRAIN:             One row per tenure band.
-- ============================================================

SELECT
    tenure_band                                       AS tenure_band,
    COUNT(*)                                          AS total_employees,
    SUM(attrition_flag)                               AS leavers,
    COUNT(*) - SUM(attrition_flag)                    AS stayers,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2)  AS attrition_rate_pct,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*) - 16.12, 2) AS gap_vs_company_pp
FROM fact_employee
GROUP BY tenure_band
ORDER BY attrition_rate_pct DESC;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- Same structure as Queries 02 and 03.  This time the group is
-- tenure_band — the derived column we built in Stage 3 with
-- bands: '0-1 years', '2-3 years', '4-5 years', '6-10 years',
-- '10+ years'.
--
-- KEY POINT — WHY TENURE MATTERS:
--   Attrition is almost never uniform across tenure.  Usually
--   there's an "early cliff" (first 1-2 years) and a "mid-career
--   dip" (years 4-7).  Knowing WHERE the cliff is tells HR
--   WHEN to intervene — onboarding fixes the cliff, career
--   development fixes the dip.  Different problems, different
--   solutions.
--
-- REMINDER ON SORTING:
--   We sort by attrition_rate_pct DESC, not by tenure_band,
--   because the business question is "where is the worst
--   attrition?" — not "walk me through tenure in order."
--   The band order ('0-1' before '2-3') is a secondary concern.
-- ============================================================