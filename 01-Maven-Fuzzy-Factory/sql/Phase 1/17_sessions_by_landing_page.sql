SELECT
    wp.pageview_url AS landing_page,
    COUNT(*) AS sessions
FROM
(
    SELECT
        website_session_id,
        MIN(website_pageview_id) AS first_pageview_id
    FROM website_pageviews
    GROUP BY website_session_id
) AS first_pageviews
INNER JOIN website_pageviews AS wp
    ON first_pageviews.first_pageview_id = wp.website_pageview_id
GROUP BY wp.pageview_url
ORDER BY sessions DESC;