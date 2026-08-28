-- Query: Operator Error Downtime Percentage

-- What percentage of downtime is associated with operator-related factors?

SELECT
    CASE
        WHEN df."Operator Error" = 'Yes' THEN 'Operator Error'
        ELSE 'Non-Operator'
    END AS Error_Category,
    SUM(ld."Downtime Value") AS Total_Downtime,
    ROUND(
        SUM(ld."Downtime Value") * 100.0 /
        (SELECT SUM("Downtime Value") FROM line_downtime_prepared),
        2
    ) AS Percentage
FROM line_downtime_prepared AS ld
JOIN downtime_factors AS df
    ON ld."Downtime Factor" = df.Factor
GROUP BY Error_Category
ORDER BY Percentage DESC;


