SELECT
    IFNULL(ws.utm_source, 'Direct / Untagged') AS utm_source,

    ws.device_type,

    wp.pageview_url AS landing_page,

    COUNT(DISTINCT ws.website_session_id) AS sessions

FROM website_sessions AS ws

INNER JOIN (
    SELECT
        website_session_id,
        MIN(website_pageview_id) AS first_pageview_id

    FROM website_pageviews

    GROUP BY website_session_id

) AS first_pageviews

    ON ws.website_session_id = first_pageviews.website_session_id

INNER JOIN website_pageviews AS wp
    ON first_pageviews.first_pageview_id = wp.website_pageview_id

WHERE wp.pageview_url IN (
    '/home',
    '/lander-1',
    '/lander-2',
    '/lander-3',
    '/lander-4',
    '/lander-5'
)

GROUP BY
    IFNULL(ws.utm_source, 'Direct / Untagged'),
    ws.device_type,
    wp.pageview_url

ORDER BY
    utm_source,
    ws.device_type,

    CASE wp.pageview_url
        WHEN '/home' THEN 1
        WHEN '/lander-1' THEN 2
        WHEN '/lander-2' THEN 3
        WHEN '/lander-3' THEN 4
        WHEN '/lander-4' THEN 5
        WHEN '/lander-5' THEN 6
    END;