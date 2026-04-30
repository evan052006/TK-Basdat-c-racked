-- :name get_all_orders :many
-- :doc Get all orders for dropdown
SELECT
    o.order_id,
    c.full_name AS customer_name
FROM orders o
LEFT JOIN customer c ON o.customer_id = c.customer_id
ORDER BY o.order_id;
