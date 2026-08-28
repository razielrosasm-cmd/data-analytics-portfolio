SELECT
    landing_page,
    COUNT(*) AS sessions,
    SUM(pageviews) AS total_pageviews,
    ROUND(
        AVG(pageviews),
        2
    ) AS avg_pageviews_per_session
FROM
(
    SELECT
        wp.pageview_url AS landing_page,
        fp.website_session_id,
        COUNT(pv.website_pageview_id) AS pageviews
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
    INNER JOIN website_pageviews AS pv
        ON fp.website_session_id = pv.website_session_id
    GROUP BY
        wp.pageview_url,
        fp.website_session_id
) AS session_data
GROUP BY landing_page
ORDER BY avg_pageviews_per_session DESC;