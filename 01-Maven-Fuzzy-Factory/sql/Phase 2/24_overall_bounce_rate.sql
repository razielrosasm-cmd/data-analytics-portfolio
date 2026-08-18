SELECT
    COUNT(*) AS bounced_sessions,
    (
        SELECT COUNT(DISTINCT website_session_id)
        FROM website_sessions
    ) AS total_sessions,
    ROUND(
        COUNT(*) * 100.0 /
        (
            SELECT COUNT(DISTINCT website_session_id)
            FROM website_sessions
        ),
        2
    ) AS bounce_rate_percent
FROM
(
    SELECT
        website_session_id
    FROM website_pageviews
    GROUP BY website_session_id
    HAVING COUNT(*) = 1
) AS bounced_sessions;
