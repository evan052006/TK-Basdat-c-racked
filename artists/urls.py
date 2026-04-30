from django.urls import path
from .views import (
    artist_page,
    get_artists_count,
    get_genre_count,
    get_performing_artists_count,
    get_artists,
    create_artist,
    update_artist,
    delete_artist,
)

app_name = "artists"

urlpatterns = [
    path("list/", artist_page, name="list"),
    path("api/get_all/", get_artists, name="all_artist"),
    path("api/artist_count/", get_artists_count, name="artist_count"),
    path("api/genre_count/", get_genre_count, name="genre_count"),
    path(
        "api/event_artist_count/",
        get_performing_artists_count,
        name="event_artist_count",
    ),
    path("api/add_artist/", create_artist, name="add_artist"),
    path("api/update_artist/", update_artist, name="update_artist"),
    path("api/delete_artist/", delete_artist, name="delete_artist"),
]
