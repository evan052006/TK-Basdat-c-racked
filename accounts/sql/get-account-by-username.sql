-- :name get_acc_by_username :one
-- :doc Get user account from username
SELECT user_id, username, password FROM USER_ACCOUNT WHERE username=:username
