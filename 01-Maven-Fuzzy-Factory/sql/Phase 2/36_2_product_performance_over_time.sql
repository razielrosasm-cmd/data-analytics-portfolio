SELECT
    p.product_id,
    p.product_name,
    p.created_at AS product_launch_date,
    strftime('%Y-%m', oi.created_at) AS month,
    COUNT(DISTINCT oi.order_id) AS orders,
    ROUND(SUM(oi.price_usd), 2) AS total_revenue

FROM products AS p

INNER JOIN order_items AS oi
ON p.product_id = oi.product_id

GROUP BY
    p.product_id,
    p.product_name,
    p.created_at,
    month

ORDER BY
    p.product_id,
    month;