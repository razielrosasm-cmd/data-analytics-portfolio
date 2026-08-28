SELECT

    strftime('%Y-%m', ws.created_at) AS month,

    COUNT(DISTINCT ws.website_session_id) AS sessions,

    COUNT(DISTINCT o.order_id) AS orders,

    ROUND(SUM(o.price_usd), 2) AS total_revenue,

    ROUND(
        SUM(o.price_usd) /
        COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value,

    ROUND(
        SUM(o.price_usd) /
        COUNT(DISTINCT ws.website_session_id),
        2
    ) AS revenue_per_session

FROM website_sessions AS ws

LEFT JOIN orders AS o
    ON ws.website_session_id = o.website_session_id

GROUP BY
    strftime('%Y-%m', ws.created_at)

ORDER BY
    month;