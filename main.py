import flask
import api
import requests
from lyricsgenius import Genius
import random
import html
import os
from dotenv import load_dotenv

load_dotenv()

app = flask.Flask(__name__)

genius = Genius(os.getenv('genius_access_token', ""))


@app.route('/')
def index():
    playlists = ["7ptNGdPb6EriG64EWXhZoc", "2JBJkOFwobFRy9HQTYP8mI", "5lZ5yLZLc3wMM4a0Uwb2Pv"]
    response = api.client.get_resource(playlists[random.randint(0, len(playlists) - 1)])
    playlist_image = response['images'][0]['url']
    playlist_name = response['name']
    playlist_description = html.unescape(response['description'])
    preview_url = None
    item = response['tracks']['items'][random.randint(0, len(response['tracks']['items']) - 1)]
    while preview_url is None:
        item = response['tracks']['items'][random.randint(0, len(response['tracks']['items']) - 1)]
        preview_url = item['track']['preview_url']
    info = item['track']['album']['release_date']
    track_image = item['track']['album']['images'][0]['url']
    track_name = item['track']['name']
    artist_name = item['track']['artists'][0]['name']
    search_term = f"{track_name} {artist_name}"
    client_access_token = os.getenv('genius_access_token', "")
    genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"
    res = requests.get(genius_search_url)
    json_data = res.json()
    lyrics_url = '#'
    is_lyrics_available = 'disabled'
    if len(json_data['response']['hits']) > 0:
        lyrics_url = json_data['response']['hits'][0]['result']['url']
        is_lyrics_available = ''

    return flask.render_template('index.html',
                                 playlist_image=playlist_image,
                                 playlist_name=playlist_name,
                                 playlist_description=playlist_description,
                                 preview_url=preview_url,
                                 track_image=track_image,
                                 track_name=track_name,
                                 artist_name=artist_name,
                                 lyrics=lyrics_url,
                                 is_lyrics_available=is_lyrics_available,
                                 info=info)


app.run(
    debug=True,
    port=int(os.getenv("PORT", "8080")),
    host=os.getenv("IP", "0.0.0.0"))
