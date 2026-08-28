SELECT
    ws.device_type,

    CASE
        WHEN wp.pageview_url IN ('/billing', '/billing-2')
            THEN '/billing'
        ELSE wp.pageview_url
    END AS funnel_stage,

    COUNT(DISTINCT wp.website_session_id) AS sessions

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
    ws.device_type,
    funnel_stage

ORDER BY
    ws.device_type,
    CASE funnel_stage
        WHEN '/products' THEN 1
        WHEN '/the-original-mr-fuzzy' THEN 2
        WHEN '/cart' THEN 3
        WHEN '/shipping' THEN 4
        WHEN '/billing' THEN 5
        WHEN '/thank-you-for-your-order' THEN 6
    END;