-- :name get_artist_in_events_count :scalar
-- :doc Get current number of artists
SELECT DISTINCT count(*) FROM artist AS a
JOIN event_artist AS ea ON ea.artist_id = a.artist_id;
