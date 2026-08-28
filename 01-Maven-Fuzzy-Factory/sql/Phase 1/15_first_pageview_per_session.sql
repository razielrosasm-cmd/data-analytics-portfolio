SELECT
    website_session_id,
    MIN(website_pageview_id) AS first_pageview_id
FROM website_pageviews
GROUP BY website_session_id
LIMIT 10;