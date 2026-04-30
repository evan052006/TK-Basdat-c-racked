-- :name get_organizer_by_user_id :one
-- :doc Get organizer profile by user_id
SELECT organizer_id, organizer_name, contact_email, user_id
FROM organizer
WHERE user_id = :user_id
