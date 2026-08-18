SELECT
    ws.device_type,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(o.price_usd), 2) AS total_revenue,
    ROUND(
        SUM(o.price_usd) /
        COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM website_sessions AS ws
LEFT JOIN orders AS o
    ON ws.website_session_id = o.website_session_id
GROUP BY ws.device_type
ORDER BY average_order_value DESC;