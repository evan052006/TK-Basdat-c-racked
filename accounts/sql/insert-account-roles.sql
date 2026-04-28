-- :name insert_roles :affected
-- :doc Assign a role onto a user
INSERT INTO account_role (user_id, role_id)
VALUES (:user_id, :role_id);
