SELECT
    IFNULL(ws.utm_source, 'Direct / Untagged') AS utm_source,

    ws.device_type,

    CASE
        WHEN wp.pageview_url IN ('/billing', '/billing-2')
        THEN '/billing'
        ELSE wp.pageview_url
    END AS funnel_stage,

    COUNT(DISTINCT ws.website_session_id) AS sessions

FROM website_sessions AS ws

INNER JOIN website_pageviews AS wp
    ON ws.website_session_id = wp.website_session_id

WHERE wp.pageview_url IN (
    '/products',
    '/the-original-mr-fuzzy',
    '/cart',
    '/shipping',
    '/billing',
    '/billing-2',
    '/thank-you-for-your-order'
)

GROUP BY
    IFNULL(ws.utm_source, 'Direct / Untagged'),
    ws.device_type,

    CASE
        WHEN wp.pageview_url IN ('/billing', '/billing-2')
        THEN '/billing'
        ELSE wp.pageview_url
    END

ORDER BY
    utm_source,
    ws.device_type,

    CASE
        WHEN wp.pageview_url = '/products' THEN 1
        WHEN wp.pageview_url = '/the-original-mr-fuzzy' THEN 2
        WHEN wp.pageview_url = '/cart' THEN 3
        WHEN wp.pageview_url = '/shipping' THEN 4
        WHEN wp.pageview_url IN ('/billing', '/billing-2') THEN 5
        WHEN wp.pageview_url = '/thank-you-for-your-order' THEN 6
    END;