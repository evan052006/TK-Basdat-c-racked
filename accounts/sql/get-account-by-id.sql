-- :name get_acc_by_id :one
-- :doc Get user account from id
SELECT user_id, username, password FROM user_account WHERE user_id=:user_id
