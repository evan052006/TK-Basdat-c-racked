-- :name get_customer_by_user_id :one
-- :doc Get customer profile by user_id
SELECT customer_id, full_name, phone_number, user_id
FROM customer
WHERE user_id = :user_id
