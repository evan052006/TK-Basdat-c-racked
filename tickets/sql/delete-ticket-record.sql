-- :name delete_ticket_record :affected
-- :doc Delete a ticket record
DELETE FROM ticket WHERE ticket_id = :ticket_id;
