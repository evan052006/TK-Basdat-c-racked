-- :name delete_order :affected
DELETE FROM TIKTAKTUK.ORDERS
WHERE order_id = :order_id;
