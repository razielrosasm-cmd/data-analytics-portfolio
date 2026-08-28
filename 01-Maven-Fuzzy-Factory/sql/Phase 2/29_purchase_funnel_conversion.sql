SELECT
    funnel_stage,
    sessions,

    CASE
        WHEN funnel_stage = '/products' THEN NULL

        WHEN funnel_stage = '/the-original-mr-fuzzy' THEN
            ROUND(
                sessions * 100.0 /
                (
                    SELECT COUNT(DISTINCT website_session_id)
                    FROM website_pageviews
                    WHERE pageview_url = '/products'
                ),
                2
            )

        WHEN funnel_stage = '/cart' THEN
            ROUND(
                sessions * 100.0 /
                (
                    SELECT COUNT(DISTINCT website_session_id)
                    FROM website_pageviews
                    WHERE pageview_url = '/the-original-mr-fuzzy'
                ),
                2
            )

        WHEN funnel_stage = '/shipping' THEN
            ROUND(
                sessions * 100.0 /
                (
                    SELECT COUNT(DISTINCT website_session_id)
                    FROM website_pageviews
                    WHERE pageview_url = '/cart'
                ),
                2
            )

        WHEN funnel_stage = '/billing' THEN
            ROUND(
                sessions * 100.0 /
                (
                    SELECT COUNT(DISTINCT website_session_id)
                    FROM website_pageviews
                    WHERE pageview_url = '/shipping'
                ),
                2
            )

        WHEN funnel_stage = '/thank-you-for-your-order' THEN
            ROUND(
                sessions * 100.0 /
                (
                    SELECT COUNT(DISTINCT website_session_id)
                    FROM website_pageviews
                    WHERE pageview_url IN ('/billing', '/billing-2')
                ),
                2
            )
    END AS conversion_rate_percent

FROM
(
    SELECT
        CASE
            WHEN pageview_url IN ('/billing', '/billing-2')
                THEN '/billing'
            ELSE pageview_url
        END AS funnel_stage,

        COUNT(DISTINCT website_session_id) AS sessions

    FROM website_pageviews

    WHERE pageview_url IN (
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
            WHEN '/products' THEN 1
            WHEN '/the-original-mr-fuzzy' THEN 2
            WHEN '/cart' THEN 3
            WHEN '/shipping' THEN 4
            WHEN '/billing' THEN 5
            WHEN '/thank-you-for-your-order' THEN 6
        END
);