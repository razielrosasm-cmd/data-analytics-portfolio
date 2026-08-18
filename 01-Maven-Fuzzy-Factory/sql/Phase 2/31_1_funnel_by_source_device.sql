SELECT
    utm_source,
    device_type,
    funnel_stage,
    sessions,

    CASE
        WHEN funnel_stage = '/products' THEN NULL

        WHEN funnel_stage = '/the-original-mr-fuzzy' THEN
            ROUND(
                sessions * 100.0 /
                (
                    SELECT COUNT(DISTINCT wp.website_session_id)
                    FROM website_sessions AS ws
                    INNER JOIN website_pageviews AS wp
                        ON ws.website_session_id = wp.website_session_id
                    WHERE IFNULL(ws.utm_source, 'Direct / Untagged') = fd.utm_source
                    AND ws.device_type = fd.device_type
                    AND wp.pageview_url = '/products'
                ),
                2
            )

        WHEN funnel_stage = '/cart' THEN
            ROUND(
                sessions * 100.0 /
                (
                    SELECT COUNT(DISTINCT wp.website_session_id)
                    FROM website_sessions AS ws
                    INNER JOIN website_pageviews AS wp
                        ON ws.website_session_id = wp.website_session_id
                    WHERE IFNULL(ws.utm_source, 'Direct / Untagged') = fd.utm_source
                    AND ws.device_type = fd.device_type
                    AND wp.pageview_url = '/the-original-mr-fuzzy'
                ),
                2
            )

        WHEN funnel_stage = '/shipping' THEN
            ROUND(
                sessions * 100.0 /
                (
                    SELECT COUNT(DISTINCT wp.website_session_id)
                    FROM website_sessions AS ws
                    INNER JOIN website_pageviews AS wp
                        ON ws.website_session_id = wp.website_session_id
                    WHERE IFNULL(ws.utm_source, 'Direct / Untagged') = fd.utm_source
                    AND ws.device_type = fd.device_type
                    AND wp.pageview_url = '/cart'
                ),
                2
            )

        WHEN funnel_stage = '/billing' THEN
            ROUND(
                sessions * 100.0 /
                (
                    SELECT COUNT(DISTINCT wp.website_session_id)
                    FROM website_sessions AS ws
                    INNER JOIN website_pageviews AS wp
                        ON ws.website_session_id = wp.website_session_id
                    WHERE IFNULL(ws.utm_source, 'Direct / Untagged') = fd.utm_source
                    AND ws.device_type = fd.device_type
                    AND wp.pageview_url = '/shipping'
                ),
                2
            )

        WHEN funnel_stage = '/thank-you-for-your-order' THEN
            ROUND(
                sessions * 100.0 /
                (
                    SELECT COUNT(DISTINCT wp.website_session_id)
                    FROM website_sessions AS ws
                    INNER JOIN website_pageviews AS wp
                        ON ws.website_session_id = wp.website_session_id
                    WHERE IFNULL(ws.utm_source, 'Direct / Untagged') = fd.utm_source
                    AND ws.device_type = fd.device_type
                    AND wp.pageview_url IN ('/billing', '/billing-2')
                ),
                2
            )
    END AS conversion_rate_percent

FROM
(
    SELECT
        IFNULL(ws.utm_source, 'Direct / Untagged') AS utm_source,
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
        IFNULL(ws.utm_source, 'Direct / Untagged'),
        ws.device_type,
        funnel_stage
) AS fd

ORDER BY
    utm_source,
    device_type,
    CASE funnel_stage
        WHEN '/products' THEN 1
        WHEN '/the-original-mr-fuzzy' THEN 2
        WHEN '/cart' THEN 3
        WHEN '/shipping' THEN 4
        WHEN '/billing' THEN 5
        WHEN '/thank-you-for-your-order' THEN 6
    END;