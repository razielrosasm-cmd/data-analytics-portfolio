-- ============================================================================
-- Track C | Query C7 — High-risk cell: truck age × monthly mileage
-- ============================================================================
-- Business question : Where does maintenance cost concentrate in the
--                     intersection of truck age and monthly mileage?
-- Why this matters  : This is the high-risk cell cross-tab required by the
--                     master prompt workflow. If a cell (e.g. 7+ years AND
--                     20k+ mi) shows average cost 2x the fleet mean with
--                     enough truck-months to be significant, that cell is a
--                     genuine operational finding and becomes the "avoid this
--                     profile" recommendation.
-- Expected output   : Up to 25 rows — every (age_band x miles_band) combination.
-- Export target     : sql/analysis/results/track_c_07_high_risk_cell.csv
-- Tool bounds       : SELECT + CASE + CASE + GROUP BY + ORDER BY.
-- ============================================================================

SELECT
    CASE
        WHEN truck_age_years < 5                            THEN '1. under 5 yrs'
        WHEN truck_age_years BETWEEN 5 AND 7.99             THEN '2. 5-8 yrs'
        ELSE                                                     '3. 8+ yrs'
    END                                                     AS age_band,
    CASE
        WHEN total_miles < 10000                            THEN '1. under 10k'
        WHEN total_miles BETWEEN 10000 AND 19999            THEN '2. 10-20k'
        ELSE                                                     '3. 20k+'
    END                                                     AS miles_band,
    COUNT(*)                                                AS truck_months,
    ROUND(AVG(maintenance_cost), 2)                         AS avg_cost,
    ROUND(AVG(downtime_hours), 1)                           AS avg_downtime_hours,
    ROUND(SUM(high_maintenance_flag) * 100.0 / COUNT(*), 2) AS high_maint_pct
FROM master_truck_month_clean
GROUP BY age_band, miles_band
ORDER BY age_band, miles_band;