SELECT
    p.product_id,
    p.product_name,
    COUNT(DISTINCT oi.order_id) AS orders,
    SUM(oi.is_primary_item) AS primary_item_count,
    ROUND(SUM(oi.price_usd), 2) AS total_revenue,
    ROUND(
        SUM(oi.price_usd) / COUNT(DISTINCT oi.order_id),
        2
    ) AS revenue_per_order,
    ROUND(
        SUM(oi.is_primary_item) * 1.0 / COUNT(DISTINCT oi.order_id),
        2
    ) AS primary_item_ratio

FROM products AS p

LEFT JOIN order_items AS oi
ON p.product_id = oi.product_id

GROUP BY
    p.product_id,
    p.product_name

ORDER BY
    total_revenue DESC;