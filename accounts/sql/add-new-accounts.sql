-- :name create_user :insert
-- :doc Assign multiple roles onto a user
INSERT INTO ACCOUNT_ROLES (username, password)
VALUES (:username, :password)
RETURNING user_id;
