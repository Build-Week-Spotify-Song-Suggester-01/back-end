from flask import Flask, render_template, request
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os

   
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

token = SpotifyClientCredentials(
    client_id="516dcc7dd59a48eb85604f46f2aa134a",
    client_secret="4326ec02ca5e4df6b46066bb774006a4")
sp = spotipy.Spotify(auth_manager=token)


@app.route('/', methods=["POST","GET"])
def home():
    name = request.form.get('song_name')
    artist = ''
    artist_href = ''
    if name:
        song = sp.search(q=name)
        artist = song['tracks']['items'][0]['album']['artists'][0]['name']
        artist_href = song['tracks']['items'][0]['album']['artists'][0]['external_urls']['spotify']
    return render_template('home.html', artist=artist, artist_href=artist_href)
