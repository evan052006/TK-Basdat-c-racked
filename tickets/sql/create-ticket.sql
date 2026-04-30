-- :name create_ticket :one
-- :doc Create a new ticket
INSERT INTO ticket (code, tcategory_id, torder_id)
VALUES (:code, :tcategory_id, :torder_id)
RETURNING ticket_id, code, tcategory_id, torder_id;
