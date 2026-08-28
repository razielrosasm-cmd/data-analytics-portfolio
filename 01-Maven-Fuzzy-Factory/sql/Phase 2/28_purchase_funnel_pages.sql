SELECT
    CASE
        WHEN pageview_url IN ('/billing', '/billing-2')
            THEN '/billing'
        ELSE pageview_url
    END AS funnel_stage,

    COUNT(DISTINCT website_session_id) AS sessions

FROM website_pageviews

WHERE pageview_url IN (
    '/home',
    '/products',
    '/the-original-mr-fuzzy',
    '/cart',
    '/shipping',
    '/billing',
    '/billing-2',
    '/thank-you-for-your-order'
)

GROUP BY funnel_stage

ORDER BY
    CASE funnel_stage
        WHEN '/home' THEN 1
        WHEN '/products' THEN 2
        WHEN '/the-original-mr-fuzzy' THEN 3
        WHEN '/cart' THEN 4
        WHEN '/shipping' THEN 5
        WHEN '/billing' THEN 6
        WHEN '/thank-you-for-your-order' THEN 7
    END;