-- Query: Utilization by Day

-- How does daily utilization vary?

SELECT
    lp.Date,
    ROUND(
        SUM(p."Min batch time") * 100.0 /
        SUM(
            SUBSTR(lp."Actual Batch Time", 8, 2) * 60
            + SUBSTR(lp."Actual Batch Time", 11, 2)
        ),
        2
    ) AS Daily_Utilization_Pct
FROM line_productivity_prepared AS lp
JOIN products AS p
    ON lp.Product = p.Product
GROUP BY lp.Date
ORDER BY lp.Date;