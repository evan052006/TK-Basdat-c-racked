-- :name get_promotions :many
SELECT promotion_id, promo_code, discount_type, discount_value, start_date, end_date, usage_limit
FROM TIKTAKTUK.PROMOTION
ORDER BY promo_code;
