-- :name update_user_password :affected
-- :doc Update user password hash
UPDATE user_account
SET password = :password
WHERE user_id = :user_id
