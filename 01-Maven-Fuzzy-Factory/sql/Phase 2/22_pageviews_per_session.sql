SELECT
    website_session_id,
    COUNT(*) AS pageviews
FROM website_pageviews
GROUP BY website_session_id
LIMIT 20;