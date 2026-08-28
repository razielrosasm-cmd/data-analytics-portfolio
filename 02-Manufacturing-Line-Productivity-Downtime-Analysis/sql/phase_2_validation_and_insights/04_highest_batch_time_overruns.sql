-- Query 01: Batches with the highest production-time overruns

-- Which batches had the largest production-time overruns?

SELECT
    lp.Product,
    lp.Batch,
    (
        SUBSTR(lp."Actual Batch Time", 8, 2) * 60
        + SUBSTR(lp."Actual Batch Time", 11, 2)
    ) AS Actual_Minutes,
    p."Min batch time" AS Standard_Minutes,
    ROUND(
        (
            SUBSTR(lp."Actual Batch Time", 8, 2) * 60
            + SUBSTR(lp."Actual Batch Time", 11, 2)
        ) - p."Min batch time",
        2
    ) AS Time_Variance
FROM line_productivity_prepared AS lp
JOIN products AS p
    ON lp.Product = p.Product
ORDER BY Time_Variance DESC
LIMIT 10;