-- :name get_artist_by_id :one
-- :doc Get single artist by ID
SELECT artist_id, name, genre FROM artist
WHERE artist_id = :artist_id;
