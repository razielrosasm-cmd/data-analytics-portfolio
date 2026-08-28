-- Query 01: Top 5 downtime factors concentration

-- How much of total downtime is concentrated in the top 5 factors?

SELECT
    SUM(Total_Downtime) AS Top_5_Downtime,
    (
        SELECT SUM("Downtime Value")
        FROM line_downtime_prepared
    ) AS Total_Downtime,
    ROUND(
        SUM(Total_Downtime) * 100.0 /
        (
            SELECT SUM("Downtime Value")
            FROM line_downtime_prepared
        ),
        2
    ) AS Top_5_Downtime_Pct
FROM (
    SELECT
        "Downtime Factor",
        SUM("Downtime Value") AS Total_Downtime
    FROM line_downtime_prepared
    GROUP BY "Downtime Factor"
    ORDER BY Total_Downtime DESC
    LIMIT 5
);