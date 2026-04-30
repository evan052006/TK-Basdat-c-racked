-- :name create_promotion :one
INSERT INTO TIKTAKTUK.PROMOTION (
    promo_code, discount_type, discount_value, start_date, end_date, usage_limit
)
VALUES (:promo_code, :discount_type, :discount_value, :start_date, :end_date, :usage_limit)
RETURNING promotion_id, promo_code, discount_type, discount_value, start_date, end_date, usage_limit;
