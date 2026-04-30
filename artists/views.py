from django.shortcuts import render
import json
from django.http import JsonResponse
from accounts.decorators import require_roles
from django.views.decorators.http import require_POST
from .queries import artists_db


@require_roles("GUEST", "CUSTOMER", "ORGANIZER", "ADMIN")
def artist_page(request):
    return render(request, "artists_list.html")


@require_POST
@require_roles("ADMIN")
def create_artist(request):
    data = json.loads(request.body)

    name = data.get("name")
    genre = data.get("genre")

    artists_db.create_artist(name=name, genre=genre)

    return JsonResponse({"status": "success"}, status=200)


@require_POST
@require_roles("ADMIN")
def update_artist(request):
    data = json.loads(request.body)

    artist_id = data.get("artist_id")
    name = data.get("name")
    genre = data.get("genre", "")

    if not artist_id or not name:
        return JsonResponse({"status": "error", "message": "Missing required fields"}, status=400)

    artists_db.update_artist(artist_id=artist_id, name=name, genre=genre)

    return JsonResponse({"status": "success"}, status=200)


@require_POST
@require_roles("ADMIN")
def delete_artist(request):
    data = json.loads(request.body)

    artist_id = data.get("artist_id")

    if not artist_id:
        return JsonResponse({"status": "error", "message": "Missing artist_id"}, status=400)

    artists_db.delete_artist(artist_id=artist_id)

    return JsonResponse({"status": "success"}, status=200)


@require_roles("GUEST", "CUSTOMER", "ORGANIZER", "ADMIN")
def get_artists(request):
    query = request.GET.get("query")
    if query == "":
        artists = artists_db.get_artists()
    else:
        artists = artists_db.get_artists_by_name(pattern=f"%{query}%")
    return JsonResponse({"status": "success", "artists": list(artists)}, status=200)


@require_roles("GUEST", "CUSTOMER", "ORGANIZER", "ADMIN")
def get_artists_count(request):
    total_artists = artists_db.get_artist_count()
    return JsonResponse(
        {"status": "success", "total_artists": total_artists}, status=200
    )


@require_roles("GUEST", "CUSTOMER", "ORGANIZER", "ADMIN")
def get_genre_count(request):
    total_genres = artists_db.get_genre_count()
    return JsonResponse({"status": "success", "total_genre": total_genres}, status=200)


@require_roles("GUEST", "CUSTOMER", "ORGANIZER", "ADMIN")
def get_performing_artists_count(request):
    total_artists = artists_db.get_artist_in_events_count()
    return JsonResponse(
        {"status": "success", "total_artists": total_artists}, status=200
    )
