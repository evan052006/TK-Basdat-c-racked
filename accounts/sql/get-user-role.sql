-- :name get_user_role :scalar
-- :doc Returns what role a user has by user_id (NOTE, ASUMSI 1 USER 1 ROLE)
SELECT role_name FROM role AS r
JOIN account_role AS ar ON r.role_id = ar.role_id
WHERE ar.user_id = :user_id
LIMIT 1;
