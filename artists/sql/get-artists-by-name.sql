-- :name get_artists_by_name :many
-- :doc Get all current artists by pattern
SELECT artist_id, name, genre FROM artist
WHERE name ILIKE :pattern OR genre ILIKE :pattern;
