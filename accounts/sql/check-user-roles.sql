-- :name has_any_role :scalar
-- :doc Returns True if the user has any of the provided roles, else False
SELECT EXISTS (
    SELECT 1 FROM account_role AS ar
    JOIN role AS r ON r.role_id = ar.role_id
    WHERE ar.user_id = :user_id AND r.role_name IN :role_names
);
