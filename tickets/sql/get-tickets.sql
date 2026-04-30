-- :name get_tickets :many
-- :doc Get all tickets with full join info
SELECT
    t.ticket_id,
    t.code,
    t.tcategory_id,
    t.torder_id,
    tc.name AS category_name,
    tc.price AS category_price,
    tc.quota AS category_quota,
    e.event_name,
    e.event_date,
    v.name AS venue_name,
    c.full_name AS customer_name,
    o.order_id,
    o.payment_status
FROM ticket t
JOIN ticket_category tc ON t.tcategory_id = tc.tcategory_id
JOIN event e ON tc.event_id = e.event_id
JOIN venue v ON e.venue_id = v.venue_id
JOIN orders o ON t.torder_id = o.order_id
LEFT JOIN customer c ON o.customer_id = c.customer_id
ORDER BY t.code;
