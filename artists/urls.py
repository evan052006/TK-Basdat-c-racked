from django.urls import path
from .views import (
    artist_page,
    get_artists_count,
    get_genre_count,
    get_performing_artists_count,
    get_artists,
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
]
