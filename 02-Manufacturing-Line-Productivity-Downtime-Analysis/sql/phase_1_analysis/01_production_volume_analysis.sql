-- Query 01: Total production batches by product

-- How many batches were produced for each product?

SELECT
    Product,
    COUNT(*) AS Total_Batches
FROM line_productivity_prepared
GROUP BY Product
ORDER BY Total_Batches DESC;