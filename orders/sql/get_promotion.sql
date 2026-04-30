-- :name get_promotion :one
SELECT promotion_id, promo_code, discount_type, discount_value, start_date, end_date, usage_limit
FROM TIKTAKTUK.PROMOTION
WHERE promotion_id = :promotion_id;
