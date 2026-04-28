-- :name create_user :scalar
-- :doc Assign multiple roles onto a user
INSERT INTO user_account (username, password)
VALUES (:username, :password)
RETURNING user_id;
