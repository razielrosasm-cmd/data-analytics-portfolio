-- Query 01: Production-time variance by operator

-- How does average production-time variance differ across operators?

SELECT
    lp.Operator,
    COUNT(*) AS Total_Batches,
    ROUND(AVG(
        SUBSTR(lp."Actual Batch Time", 8, 2) * 60
        + SUBSTR(lp."Actual Batch Time", 11, 2)
    ), 2) AS Avg_Actual_Minutes,
    ROUND(AVG(p."Min batch time"), 2) AS Avg_Standard_Minutes,
    ROUND(AVG(
        SUBSTR(lp."Actual Batch Time", 8, 2) * 60
        + SUBSTR(lp."Actual Batch Time", 11, 2)
        - p."Min batch time"
    ), 2) AS Avg_Time_Variance,
    ROUND(AVG(
        (
            (
                SUBSTR(lp."Actual Batch Time", 8, 2) * 60
                + SUBSTR(lp."Actual Batch Time", 11, 2)
            ) - p."Min batch time"
        ) * 100.0 / p."Min batch time"
    ), 2) AS Avg_Time_Variance_Pct
FROM line_productivity_prepared AS lp
JOIN products AS p
    ON lp.Product = p.Product
GROUP BY lp.Operator
ORDER BY Avg_Time_Variance DESC;