-- Query 01: Overall production efficiency

-- What is the average production-time variance across all batches?

SELECT
    COUNT(*) AS Total_Batches,
    ROUND(AVG(
        SUBSTR("Actual Batch Time", 8, 2) * 60
        + SUBSTR("Actual Batch Time", 11, 2)
    ), 2) AS Avg_Actual_Minutes,
    ROUND(AVG(p."Min batch time"), 2) AS Avg_Standard_Minutes,
    ROUND(AVG(
        SUBSTR("Actual Batch Time", 8, 2) * 60
        + SUBSTR("Actual Batch Time", 11, 2)
        - p."Min batch time"
    ), 2) AS Avg_Time_Variance,
    ROUND(AVG(
        (
            (
                SUBSTR("Actual Batch Time", 8, 2) * 60
                + SUBSTR("Actual Batch Time", 11, 2)
            ) - p."Min batch time"
        ) * 100.0 / p."Min batch time"
    ), 2) AS Avg_Time_Variance_Pct
FROM line_productivity_prepared AS lp
JOIN products AS p
    ON lp.Product = p.Product;