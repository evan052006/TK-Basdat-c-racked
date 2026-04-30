-- :name delete_ticket :affected
-- :doc Delete a ticket by ID (also removes seat relationship via cascade or manual)
DELETE FROM has_relationship WHERE ticket_id = :ticket_id;
