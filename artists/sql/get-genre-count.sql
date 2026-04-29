-- :name get_genre_count :scalar
-- :doc Get current number of distinct genres
SELECT count(DISTINCT genre) FROM artist
