-- :name get_role_by_id :one
-- :doc Get role by id
SELECT role_id, role_name FROM ROLE WHERE role_id = :role_id;
