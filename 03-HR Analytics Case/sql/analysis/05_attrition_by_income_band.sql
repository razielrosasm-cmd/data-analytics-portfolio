-- ============================================================
-- 05 — Attrition by Income Band
-- ============================================================
-- BUSINESS QUESTION: Does attrition concentrate in a particular
--                    income band?  Specifically — are lower-paid
--                    employees leaving more, or is the pattern
--                    more nuanced?
-- METRIC:            Attrition rate by monthly-income band.
-- GRAIN:             One row per income band.
-- ============================================================

SELECT
    CASE
        WHEN monthly_income < 20000  THEN '1. Low (10k-20k)'
        WHEN monthly_income < 40000  THEN '2. Lower-Mid (20k-40k)'
        WHEN monthly_income < 70000  THEN '3. Mid (40k-70k)'
        WHEN monthly_income < 120000 THEN '4. Upper-Mid (70k-120k)'
        ELSE                              '5. High (120k-200k)'
    END                                               AS income_band,
    COUNT(*)                                          AS total_employees,
    SUM(attrition_flag)                               AS leavers,
    COUNT(*) - SUM(attrition_flag)                    AS stayers,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2)  AS attrition_rate_pct,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*) - 16.12, 2) AS gap_vs_company_pp
FROM fact_employee
GROUP BY income_band
ORDER BY income_band;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- CASE WHEN ... THEN ... END
--     -> creates a label for each employee based on their
--        monthly_income.  This is BANDING or BINNING.
--        You already know CASE — this is the same tool applied
--        to a continuous number to turn it into categories.
--
-- HOW THE BANDS WERE CHOSEN:
--     -> NOT by guessing.  We first ran:
--          MIN(monthly_income) -> 10090
--          MAX(monthly_income) -> 199990
--          AVG(monthly_income) -> 65029
--        Then chose bands that actually split the population.
--        My FIRST attempt used 3k/6k/10k/20k thresholds and
--        produced 2 rows — almost everyone fell into the top
--        band.  Lesson: look at the distribution BEFORE you
--        band, not after.
--
-- '1. Low (10k-20k)' with the number prefix
--     -> forces alphabetical ORDER BY to match logical order.
--        Without the prefix, 'High' sorts before 'Low'.
--
-- GROUP BY income_band
--     -> groups by the alias from SELECT.  SQLite allows this;
--        some databases don't.
--
-- ORDER BY income_band
--     -> sort by band (low to high), NOT by attrition rate.
--        We want to SEE the income gradient; sorting by rate
--        would scramble the bands and hide it.
-- ============================================================