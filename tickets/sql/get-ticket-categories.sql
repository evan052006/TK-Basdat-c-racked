-- :name get_ticket_categories :many
-- :doc Get all ticket categories
SELECT
    tc.tcategory_id,
    tc.name,
    tc.quota,
    tc.price,
    tc.event_id,
    e.event_name
FROM ticket_category tc
JOIN event e ON tc.event_id = e.event_id
ORDER BY e.event_name, tc.name;
