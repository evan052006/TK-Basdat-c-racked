-- :name get_valid_ticket_count :scalar
-- :doc Get count of valid (PAID) tickets
SELECT count(*) FROM ticket t
JOIN orders o ON t.torder_id = o.order_id
WHERE o.payment_status = 'PAID';
