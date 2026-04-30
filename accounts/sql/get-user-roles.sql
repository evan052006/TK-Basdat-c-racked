-- :name get_user_roles :many
-- :doc Returns all roles for a user
SELECT r.role_id, r.role_name
FROM ROLE AS r
JOIN ACCOUNT_ROLE AS ar ON r.role_id = ar.role_id
WHERE ar.user_id = :user_id
ORDER BY
    CASE r.role_name
        WHEN 'CUSTOMER' THEN 1
        WHEN 'ORGANIZER' THEN 2
        WHEN 'ADMIN' THEN 3
        ELSE 99
    END;
