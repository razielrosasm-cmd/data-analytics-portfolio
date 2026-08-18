SELECT
    wp.pageview_url AS landing_page,
    COUNT(DISTINCT fp.website_session_id) AS sessions,
    ROUND(SUM(o.price_usd), 2) AS total_revenue,
    ROUND(
        SUM(o.price_usd) /
        COUNT(DISTINCT fp.website_session_id),
        2
    ) AS revenue_per_session
FROM
(
    SELECT
        website_session_id,
        MIN(website_pageview_id) AS first_pageview_id
    FROM website_pageviews
    GROUP BY website_session_id
) AS fp
INNER JOIN website_pageviews AS wp
    ON fp.first_pageview_id = wp.website_pageview_id
LEFT JOIN orders AS o
    ON fp.website_session_id = o.website_session_id
GROUP BY wp.pageview_url
ORDER BY revenue_per_session DESC;