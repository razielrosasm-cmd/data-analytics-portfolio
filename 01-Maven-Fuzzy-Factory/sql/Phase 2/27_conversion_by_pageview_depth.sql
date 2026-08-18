SELECT
    CASE
        WHEN session_data.pageviews = 1 THEN '1 pageview'
        WHEN session_data.pageviews = 2 THEN '2 pageviews'
        WHEN session_data.pageviews BETWEEN 3 AND 4 THEN '3-4 pageviews'
        ELSE '5+ pageviews'
    END AS engagement_level,

    COUNT(*) AS sessions,

    SUM(
        CASE
            WHEN session_data.order_id IS NOT NULL THEN 1
            ELSE 0
        END
    ) AS orders,

    ROUND(
        SUM(
            CASE
                WHEN session_data.order_id IS NOT NULL THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS conversion_rate_percent

FROM
(
    SELECT
        wp.website_session_id,
        COUNT(wp.website_pageview_id) AS pageviews,
        MIN(o.order_id) AS order_id

    FROM website_pageviews AS wp

    LEFT JOIN orders AS o
        ON wp.website_session_id = o.website_session_id

    GROUP BY wp.website_session_id
) AS session_data

GROUP BY engagement_level

ORDER BY
    CASE engagement_level
        WHEN '1 pageview' THEN 1
        WHEN '2 pageviews' THEN 2
        WHEN '3-4 pageviews' THEN 3
        WHEN '5+ pageviews' THEN 4
    END;