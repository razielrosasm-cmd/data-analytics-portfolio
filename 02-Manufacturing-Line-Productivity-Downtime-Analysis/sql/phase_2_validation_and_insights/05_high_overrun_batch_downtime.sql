-- Query 01: Downtime factors associated with the highest-overrun batches

-- Which downtime factors were associated with the largest production overruns?

SELECT
    lp.Product,
    ld.Batch,
    df.Description,
    ld."Downtime Value"
FROM line_downtime_prepared AS ld
JOIN line_productivity_prepared AS lp
    ON ld.Batch = lp.Batch
JOIN downtime_factors AS df
    ON ld."Downtime Factor" = df.Factor
WHERE ld.Batch IN (
    422147,
    422111,
    422123,
    422140,
    422146,
    422118,
    422143,
    422144,
    422120,
    422128
)
ORDER BY
    ld.Batch,
    ld."Downtime Value" DESC;