-- ===========================================================
-- PHASE 2
-- DATABASE EXPLORATION
-- SECTION 1
-- RECORD COUNTS
-- ===========================================================

-- Website Sessions
SELECT COUNT(*) AS total_sessions
FROM website_sessions;

-- Website Pageviews
SELECT COUNT(*) AS total_pageviews
FROM website_pageviews;

-- Orders
SELECT COUNT(*) AS total_orders
FROM orders;

-- Order Items
SELECT COUNT(*) AS total_order_items
FROM order_items;

-- Refunds
SELECT COUNT(*) AS total_refunds
FROM order_item_refunds;

-- Products
SELECT COUNT(*) AS total_products
FROM products;