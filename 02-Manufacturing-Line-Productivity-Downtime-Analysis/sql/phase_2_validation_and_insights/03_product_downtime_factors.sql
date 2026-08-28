-- Query 01: Downtime factors by product

-- Which downtime factors contribute most to downtime for each product?

SELECT
    lp.Product,
    df.Description,
    SUM(ld."Downtime Value") AS Total_Downtime
FROM line_downtime_prepared AS ld
JOIN line_productivity_prepared AS lp
    ON ld.Batch = lp.Batch
JOIN downtime_factors AS df
    ON ld."Downtime Factor" = df.Factor
GROUP BY
    lp.Product,
    df.Description
ORDER BY
    lp.Product,
    Total_Downtime DESC;