-- Query 01: Average production time variance by product

-- Which products take the longest compared with their standard batch time?

SELECT
    lp.Product,
    COUNT(*) AS Total_Batches,
    ROUND(AVG(
        SUBSTR(lp."Actual Batch Time", 8, 2) * 60
        + SUBSTR(lp."Actual Batch Time", 11, 2)
    ), 2) AS Avg_Actual_Minutes,
    p."Min batch time" AS Standard_Minutes,
    ROUND(AVG(
        SUBSTR(lp."Actual Batch Time", 8, 2) * 60
        + SUBSTR(lp."Actual Batch Time", 11, 2)
        - p."Min batch time"
    ), 2) AS Avg_Time_Variance
FROM line_productivity_prepared AS lp
JOIN products AS p
    ON lp.Product = p.Product
GROUP BY lp.Product, p."Min batch time"
ORDER BY Avg_Time_Variance DESC;


-- Query 02: Average production time variance percentage by product

-- Which products have the largest percentage variance from standard?

SELECT
    lp.Product,
    COUNT(*) AS Total_Batches,
    p."Min batch time" AS Standard_Minutes,
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
GROUP BY lp.Product, p."Min batch time"
ORDER BY Avg_Time_Variance_Pct DESC;