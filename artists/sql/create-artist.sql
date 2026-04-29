-- :name create_artist :affected
-- :doc creates new artist
INSERT INTO artist (name, genre)
VALUES (:name, :genre);
