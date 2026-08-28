-- Query: Overall Utilization

-- What is the overall production line utilization?

SELECT
    ROUND(
        SUM(p."Min batch time") * 100.0 /
        SUM(
            SUBSTR(lp."Actual Batch Time", 8, 2) * 60
            + SUBSTR(lp."Actual Batch Time", 11, 2)
        ),
        2
    ) AS Overall_Utilization_Pct,
    SUM(p."Min batch time") AS Total_Standard_Time,
    SUM(
        SUBSTR(lp."Actual Batch Time", 8, 2) * 60
        + SUBSTR(lp."Actual Batch Time", 11, 2)
    ) AS Total_Production_Time,
    SUM(
        SUBSTR(lp."Actual Batch Time", 8, 2) * 60
        + SUBSTR(lp."Actual Batch Time", 11, 2)
    ) - SUM(p."Min batch time") AS Total_Downtime
FROM line_productivity_prepared AS lp
JOIN products AS p
    ON lp.Product = p.Product;