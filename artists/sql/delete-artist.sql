-- :name delete_artist :affected
-- :doc Delete an artist by ID
DELETE FROM artist
WHERE artist_id = :artist_id;
