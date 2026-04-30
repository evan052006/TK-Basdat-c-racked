-- :name get_orders :many
SELECT o.order_id, o.order_date, o.payment_status, o.total_amount, c.full_name as customer_name
FROM TIKTAKTUK.ORDERS o
LEFT JOIN TIKTAKTUK.CUSTOMER c ON o.customer_id = c.customer_id
ORDER BY o.order_date DESC;
