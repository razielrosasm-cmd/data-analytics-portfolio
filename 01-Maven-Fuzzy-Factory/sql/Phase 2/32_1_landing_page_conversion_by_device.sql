SELECT
    ws.device_type,
    wp.pageview_url AS landing_page,

    COUNT(DISTINCT ws.website_session_id) AS sessions,

    COUNT(DISTINCT o.order_id) AS orders,

    ROUND(
        COUNT(DISTINCT o.order_id) * 100.0 /
        COUNT(DISTINCT ws.website_session_id),
        2
    ) AS conversion_rate_percent

FROM website_sessions AS ws

INNER JOIN website_pageviews AS wp
    ON ws.website_session_id = wp.website_session_id

LEFT JOIN orders AS o
    ON ws.website_session_id = o.website_session_id

WHERE wp.website_pageview_id IN (

    SELECT
        MIN(website_pageview_id)

    FROM website_pageviews

    GROUP BY website_session_id

)

AND wp.pageview_url IN (
    '/home',
    '/lander-1',
    '/lander-2',
    '/lander-3',
    '/lander-4',
    '/lander-5'
)

GROUP BY
    ws.device_type,
    wp.pageview_url

ORDER BY
    ws.device_type,

    CASE wp.pageview_url
        WHEN '/home' THEN 1
        WHEN '/lander-1' THEN 2
        WHEN '/lander-2' THEN 3
        WHEN '/lander-3' THEN 4
        WHEN '/lander-4' THEN 5
        WHEN '/lander-5' THEN 6
    END;