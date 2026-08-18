SELECT
    ws.utm_source,
    COUNT(DISTINCT ws.website_session_id) AS sessions,
    ROUND(SUM(o.price_usd), 2) AS total_revenue,
    ROUND(
        SUM(o.price_usd) /
        COUNT(DISTINCT ws.website_session_id),
        2
    ) AS revenue_per_session
FROM website_sessions AS ws
LEFT JOIN orders AS o
    ON ws.website_session_id = o.website_session_id
GROUP BY ws.utm_source
ORDER BY revenue_per_session DESC;