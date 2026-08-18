SELECT
    IFNULL(ws.utm_source, 'Direct / Untagged') AS utm_source,

    ws.device_type,

    ROUND(
        COUNT(DISTINCT CASE
            WHEN wp.pageview_url = '/the-original-mr-fuzzy'
            THEN ws.website_session_id
        END) * 100.0 /
        COUNT(DISTINCT CASE
            WHEN wp.pageview_url = '/products'
            THEN ws.website_session_id
        END),
        2
    ) AS products_to_product_detail_percent,

    ROUND(
        COUNT(DISTINCT CASE
            WHEN wp.pageview_url = '/cart'
            THEN ws.website_session_id
        END) * 100.0 /
        COUNT(DISTINCT CASE
            WHEN wp.pageview_url = '/the-original-mr-fuzzy'
            THEN ws.website_session_id
        END),
        2
    ) AS product_detail_to_cart_percent,

    ROUND(
        COUNT(DISTINCT CASE
            WHEN wp.pageview_url = '/shipping'
            THEN ws.website_session_id
        END) * 100.0 /
        COUNT(DISTINCT CASE
            WHEN wp.pageview_url = '/cart'
            THEN ws.website_session_id
        END),
        2
    ) AS cart_to_shipping_percent,

    ROUND(
        COUNT(DISTINCT CASE
            WHEN wp.pageview_url IN ('/billing', '/billing-2')
            THEN ws.website_session_id
        END) * 100.0 /
        COUNT(DISTINCT CASE
            WHEN wp.pageview_url = '/shipping'
            THEN ws.website_session_id
        END),
        2
    ) AS shipping_to_billing_percent,

    ROUND(
        COUNT(DISTINCT CASE
            WHEN wp.pageview_url = '/thank-you-for-your-order'
            THEN ws.website_session_id
        END) * 100.0 /
        COUNT(DISTINCT CASE
            WHEN wp.pageview_url IN ('/billing', '/billing-2')
            THEN ws.website_session_id
        END),
        2
    ) AS billing_to_order_percent

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
    ws.device_type

ORDER BY
    utm_source,
    ws.device_type;