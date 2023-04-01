import spotipy
from spotipy.oauth2 import SpotifyOAuth
import openai
from src.config import settings


openai.api_key = settings.openai_api_key
scope = "user-library-read,user-top-read"
GENRE = "hip hop"

MIN_ATTRIBUTES = {
    "acousticness": None,
    "danceability": None,
    "energy": None,
    "instrumentalness": None,
    "liveness": None,
    "loudness": None,
    "popularity": None,
    "speechiness": None,
    "valence": None,
}

MAX_ATTRIBUTES = {
    "acousticness": None,
    "danceability": None,
    "energy": None,
    "instrumentalness": None,
    "liveness": None,
    "loudness": None,
    "popularity": None,
    "speechiness": None,
    "valence": None,
}

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

print(f"\n\nYour favourite artists in the {GENRE} genre:\n")
for idx, item in enumerate(most_listened_artists["items"]):
    if GENRE in item["genres"]:
        artists.append(item["id"])
        artists_names.append(item["name"])
        print(idx, item["name"])

attributes = {}

for min_attribute, min_value in MIN_ATTRIBUTES.items():
    if min_value:
        attributes[f"min_{min_attribute}"] = min_value

for max_attribute, max_value in MAX_ATTRIBUTES.items():
    if max_value:
        attributes[f"max_{max_attribute}"] = max_value

recommendations = sp.recommendations(
    seed_artists=artists[::5],
    # seed_genres=[GENRE],
    limit=10,
    **attributes,
)

print(f"\n\nTop spotify suggestions:\n")
for idx, item in enumerate(recommendations["tracks"]):
    print(
        idx,
        item["name"],
        "Artists: ",
        ",".join(artist["name"] for artist in item["artists"]),
    )

artists_list = "\n".join([f"- {artist}" for artist in artists_names])

message = {
    "role": "user",
    "content": f"Can you suggest new {GENRE} artists to me if I like the following artists:\n{artists_list}",
}

print(f"\n\nChatGPT question:\n{message['content']}\n\n")

chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[message])
answer = chat_completion.choices[0].message.content
print(f"ChatGPT suggestion:\n")
print(answer)
