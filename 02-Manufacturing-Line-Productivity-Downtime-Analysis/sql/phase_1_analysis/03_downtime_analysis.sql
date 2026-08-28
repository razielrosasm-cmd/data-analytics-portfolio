-- Query 01: Total downtime by downtime factor

-- Which downtime factors contribute most to production downtime?

SELECT
    df.Factor,
    df.Description,
    SUM(ld."Downtime Value") AS Total_Downtime
FROM line_downtime_prepared AS ld
JOIN downtime_factors AS df
    ON ld."Downtime Factor" = df.Factor
GROUP BY df.Factor, df.Description
ORDER BY Total_Downtime DESC;


-- Query 02: Downtime percentage by factor

-- What percentage of total downtime does each factor represent?

SELECT
    df.Description,
    SUM(ld."Downtime Value") AS Total_Downtime,
    ROUND(
        SUM(ld."Downtime Value") * 100.0 /
        (
            SELECT SUM("Downtime Value")
            FROM line_downtime_prepared
        ),
        2
    ) AS Downtime_Pct
FROM line_downtime_prepared AS ld
JOIN downtime_factors AS df
    ON ld."Downtime Factor" = df.Factor
GROUP BY df.Description
ORDER BY Downtime_Pct DESC;


-- Query 03: Total downtime by product

-- Which products are associated with the most downtime?

SELECT
    lp.Product,
    SUM(ld."Downtime Value") AS Total_Downtime
FROM line_downtime_prepared AS ld
JOIN line_productivity_prepared AS lp
    ON ld.Batch = lp.Batch
GROUP BY lp.Product
ORDER BY Total_Downtime DESC;


-- Query 04: Average downtime per batch by product

-- Which products have the highest downtime per produced batch?

SELECT
    lp.Product,
    COUNT(DISTINCT lp.Batch) AS Total_Batches,
    SUM(ld."Downtime Value") AS Total_Downtime,
    ROUND(
        SUM(ld."Downtime Value") * 1.0 /
        COUNT(DISTINCT lp.Batch),
        2
    ) AS Avg_Downtime_Per_Batch
FROM line_downtime_prepared AS ld
JOIN line_productivity_prepared AS lp
    ON ld.Batch = lp.Batch
GROUP BY lp.Product
ORDER BY Avg_Downtime_Per_Batch DESC;