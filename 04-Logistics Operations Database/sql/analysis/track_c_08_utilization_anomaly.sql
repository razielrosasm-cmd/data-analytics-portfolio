-- ============================================================================
-- Track C | Query C8 — Utilization anomaly investigation
-- ============================================================================
-- Business question : The 13.16% of truck-months with utilization_rate > 1.0
--                     — is this a real pattern or a data artifact?
-- Why this matters  : Utilization above 100% is physically impossible for
--                     hours-based utilization. If we can explain it (e.g.
--                     it correlates with high miles, high revenue, or a
--                     particular make), it is a definitional artefact that
--                     the supervisor should know about. If it is random,
--                     it is a data-quality problem.
-- Expected output   : 2 rows — anomalous vs normal truck-months — same columns.
-- Export target     : sql/analysis/results/track_c_08_utilization_anomaly.csv
-- Tool bounds       : SELECT + CASE + GROUP BY.
-- ============================================================================

SELECT
    utilization_over_100pct,
    COUNT(*)                                                AS truck_months,
    ROUND(AVG(utilization_rate), 2)                         AS avg_utilization_rate,
    ROUND(AVG(total_miles), 0)                              AS avg_total_miles,
    ROUND(AVG(total_revenue), 0)                            AS avg_total_revenue,
    ROUND(AVG(maintenance_cost), 2)                         AS avg_maintenance_cost,
    ROUND(AVG(truck_age_years), 1)                          AS avg_truck_age_years,
    ROUND(AVG(trips_completed), 1)                          AS avg_trips
FROM master_truck_month_clean
GROUP BY utilization_over_100pct
ORDER BY utilization_over_100pct DESC;