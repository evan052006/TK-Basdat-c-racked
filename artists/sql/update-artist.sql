-- :name update_artist :affected
-- :doc Update an artist's name and genre
UPDATE artist
SET name = :name, genre = :genre
WHERE artist_id = :artist_id;
