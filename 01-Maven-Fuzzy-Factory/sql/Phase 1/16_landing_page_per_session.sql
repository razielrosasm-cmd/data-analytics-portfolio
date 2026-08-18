SELECT
    first_pageviews.website_session_id,
    wp.pageview_url AS landing_page
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
LIMIT 20;