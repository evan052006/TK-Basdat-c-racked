-- :name update_organizer_profile :affected
-- :doc Update organizer name and contact_email
UPDATE organizer
SET organizer_name = :organizer_name, contact_email = :contact_email
WHERE user_id = :user_id
