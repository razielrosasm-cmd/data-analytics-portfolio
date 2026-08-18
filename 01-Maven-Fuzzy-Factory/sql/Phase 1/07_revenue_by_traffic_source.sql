SELECT
    ws.utm_source,
    COUNT(DISTINCT ws.website_session_id) AS sessions,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(o.price_usd), 2) AS total_revenue
FROM website_sessions AS ws
LEFT JOIN orders AS o
    ON ws.website_session_id = o.website_session_id
GROUP BY ws.utm_source
ORDER BY total_revenue DESC;