-- :name update_order :one
UPDATE TIKTAKTUK.ORDERS
SET
    order_date = :order_date,
    payment_status = :payment_status,
    total_amount = :total_amount,
    customer_id = :customer_id
WHERE order_id = :order_id
RETURNING order_id, order_date, payment_status, total_amount, customer_id;
