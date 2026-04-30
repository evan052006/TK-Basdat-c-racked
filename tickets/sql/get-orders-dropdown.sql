-- :name get_orders_for_dropdown :many
-- :doc Get all orders with customer and event info for create ticket dropdown
SELECT DISTINCT
    o.order_id,
    c.full_name AS customer_name,
    e.event_name
FROM orders o
JOIN customer c ON o.customer_id = c.customer_id
JOIN ticket t2 ON t2.torder_id = o.order_id
JOIN ticket_category tc2 ON t2.tcategory_id = tc2.tcategory_id
JOIN event e ON tc2.event_id = e.event_id
ORDER BY o.order_id;
