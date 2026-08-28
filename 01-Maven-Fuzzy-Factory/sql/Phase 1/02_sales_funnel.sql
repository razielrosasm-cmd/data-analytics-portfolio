SELECT
    'Website Sessions' AS stage,
    COUNT(*) AS total
FROM website_sessions

UNION ALL

SELECT
    'Website Pageviews',
    COUNT(*)
FROM website_pageviews

UNION ALL

SELECT
    'Orders',
    COUNT(*)
FROM orders;