-- :name create_order :one
INSERT INTO TIKTAKTUK.ORDERS (order_date, payment_status, total_amount, customer_id)
VALUES (:order_date, :payment_status, :total_amount, :customer_id)
RETURNING order_id, order_date, payment_status, total_amount, customer_id;
