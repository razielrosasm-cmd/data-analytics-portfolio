SELECT

    strftime('%Y-%m', ws.created_at) AS month,

    COUNT(DISTINCT ws.website_session_id) AS sessions,

    COUNT(DISTINCT o.order_id) AS orders

FROM website_sessions AS ws

LEFT JOIN orders AS o
    ON ws.website_session_id = o.website_session_id

GROUP BY
    strftime('%Y-%m', ws.created_at)

ORDER BY
    month;