SELECT
    p.product_id,
    p.product_name,
    COUNT(DISTINCT oi.order_id) AS orders,
    SUM(oi.is_primary_item) AS primary_item_count,
    ROUND(SUM(oi.price_usd), 2) AS total_revenue

FROM products AS p

LEFT JOIN order_items AS oi
ON p.product_id = oi.product_id

GROUP BY
    p.product_id,
    p.product_name

ORDER BY
    total_revenue DESC;