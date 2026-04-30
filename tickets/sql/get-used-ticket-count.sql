-- :name get_used_ticket_count :scalar
-- :doc Get count of used tickets (those assigned to seats)
SELECT count(DISTINCT hr.ticket_id) FROM has_relationship hr;
