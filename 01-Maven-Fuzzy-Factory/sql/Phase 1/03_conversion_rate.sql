SELECT

COUNT(DISTINCT orders.website_session_id) AS converting_sessions,

COUNT(DISTINCT website_sessions.website_session_id) AS total_sessions,

ROUND(
    COUNT(DISTINCT orders.website_session_id) * 100.0 /
    COUNT(DISTINCT website_sessions.website_session_id),
2
) AS conversion_rate_percent

FROM website_sessions

LEFT JOIN orders
ON website_sessions.website_session_id = orders.website_session_id;