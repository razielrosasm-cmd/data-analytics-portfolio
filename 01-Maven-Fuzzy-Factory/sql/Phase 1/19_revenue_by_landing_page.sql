SELECT
    wp.pageview_url AS landing_page,
    COUNT(DISTINCT fp.website_session_id) AS sessions,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(o.price_usd), 2) AS total_revenue
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
ORDER BY total_revenue DESC;