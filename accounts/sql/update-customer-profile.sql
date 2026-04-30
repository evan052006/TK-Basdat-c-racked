-- :name update_customer_profile :affected
-- :doc Update customer full_name and phone_number
UPDATE customer
SET full_name = :full_name, phone_number = :phone_number
WHERE user_id = :user_id
