from fastapi import APIRouter, status
from src.models.base import RequestModel, ResponseModel
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from src.config import settings
import openai

scope = "user-library-read,user-top-read"
openai.api_key = settings.openai_api_key

router = APIRouter(
    prefix="",
    tags=["base"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post("/recomend", response_model=ResponseModel)
async def base(request: RequestModel):
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            scope=scope,
            client_id=settings.spotipy_client_id,
            client_secret=settings.spotipy_client_secret,
            redirect_uri="http://localhost:8080/callback",
            open_browser=False,
        )
    )
    most_listened_artists = sp.current_user_top_artists(limit=50, offset=0, time_range="medium_term")
    artists = []
    artists_names = []

    for item in most_listened_artists["items"]:
        if request.genre in item["genres"]:
            artists.append(item["id"])
            artists_names.append(item["name"])

    attributes = {}
    if request.min:
        for min_attribute, min_value in request.min.dict().items():
            if min_value:
                attributes[f"min_{min_attribute}"] = min_value

    if request.max:
        for max_attribute, max_value in request.max.dict().items():
            if max_value:
                attributes[f"max_{max_attribute}"] = max_value

    recommendations = sp.recommendations(
        seed_artists=artists[::5],
        limit=10,
        **attributes,
    )

    artists_ids = set()

    for item in recommendations["tracks"]:
        for artist in item["artists"]:
            artists_ids.add(artist["id"])

    artists = sp.artists(artists_ids)

    artists_images = {artist["id"]: artist.get("images", [None])[0] for artist in artists["artists"]}

    tracks = []
    for item in recommendations["tracks"]:
        tracks.append(
            {
                "name": item["name"],
                "artists": [
                    {"name": artist["name"], "image": artists_images.get(artist["id"])} for artist in item["artists"]
                ],
                "preview": item["preview_url"],
            }
        )

    artists_list = "\n".join([f"- {artist}" for artist in artists_names])

    message = {
        "role": "user",
        "content": f"Can you suggest new {request.genre} artists to me if I like the following artists:\n{artists_list}",
    }

    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[message])
    answer = chat_completion.choices[0].message.content

    return {
        # "tracks": tracks,
        "tracks": None,
        "openia": answer,
    }
