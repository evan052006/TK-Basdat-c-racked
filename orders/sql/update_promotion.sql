-- :name update_promotion :one
UPDATE TIKTAKTUK.PROMOTION
SET
    promo_code = :promo_code,
    discount_type = :discount_type,
    discount_value = :discount_value,
    start_date = :start_date,
    end_date = :end_date,
    usage_limit = :usage_limit
WHERE promotion_id = :promotion_id
RETURNING promotion_id, promo_code, discount_type, discount_value, start_date, end_date, usage_limit;
