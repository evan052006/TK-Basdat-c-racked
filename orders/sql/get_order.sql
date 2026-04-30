-- :name get_order :one
SELECT o.order_id, o.order_date, o.payment_status, o.total_amount, o.customer_id, c.full_name as customer_name
FROM TIKTAKTUK.ORDERS o
LEFT JOIN TIKTAKTUK.CUSTOMER c ON o.customer_id = c.customer_id
WHERE o.order_id = :order_id;
