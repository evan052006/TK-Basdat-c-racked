-- :name insert_roles :insert
-- :doc Assign a role onto a user
INSERT INTO ACCOUNT_ROLES (user_id, role_id)
VALUES (:user_id, :role_id);
