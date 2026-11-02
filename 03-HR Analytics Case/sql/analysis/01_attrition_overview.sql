-- ============================================================
-- 01 — Attrition Overview (KPI Layer)
-- ============================================================
-- BUSINESS QUESTION: What is our overall attrition rate, and
--                    how does it compare to the 15% benchmark
--                    stated by management?
-- METRIC:            Company-wide attrition rate + counts.
-- GRAIN:             One row (single aggregate).
-- ============================================================

SELECT
    COUNT(*)                                          AS total_employees,
    SUM(attrition_flag)                               AS total_leavers,
    COUNT(*) - SUM(attrition_flag)                    AS total_stayers,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2)  AS attrition_rate_pct,
    15.00                                             AS benchmark_pct,
    ROUND(100.0 * SUM(attrition_flag) / COUNT(*) - 15.00, 2) AS gap_vs_benchmark_pp
FROM fact_employee;


-- ============================================================
-- WHAT EACH LINE DOES  (interview prep — say it out loud)
-- ============================================================
-- COUNT(*)                    -> counts every row in fact_employee  (4,410)
-- SUM(attrition_flag)         -> sums the 0/1 flags                 (711)
-- COUNT(*) - SUM(...)         -> stayers                            (3,699)
-- 100.0 * SUM(...) / COUNT(*) -> rate, using 100.0 (not 100) so
--                                SQLite does float division, not
--                                integer division                     (16.12)
-- 15.00 AS benchmark_pct      -> a hardcoded constant so the output
--                                is self-documenting
-- ... - 15.00                 -> difference in PERCENTAGE POINTS (pp),
--                                not percent.  16.12% vs 15% is
--                                +1.12 pp, NOT "+1.12%".
--
-- WHY 100.0 AND NOT 100?
--   In SQLite, 100 * 711 / 4410 does integer arithmetic and returns
--   16, not 16.12.  The .0 forces float division.  This is a real
--   trap — remember it.
-- ============================================================