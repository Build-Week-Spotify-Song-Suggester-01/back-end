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
    song_href = ''
    album = ''
    album_href = ''
    release_date = ''
    acoustic = None
    dance = None
    energy = None
    loud = None
    live = None
    speech = None
    tempo = None
    valence = None
    if name:
        song = sp.search(q=name)
        artist = song['tracks']['items'][0]['album']['artists'][0]['name']
        artist_href = song['tracks']['items'][0]['artists'][0]['external_urls']['spotify']
        song_href = song['tracks']['items'][0]['external_urls']['spotify']
        album = song['tracks']['items'][0]['album']['name']
        album_href = song['tracks']['items'][0]['album']['external_urls']['spotify']
        release_date = song['tracks']['items'][0]['album']['release_date']
        features = sp.audio_features(song_href)
        acoustic = features[0]['acousticness']
        dance = features[0]['danceability']
        energy = features[0]['energy']
        loud = features[0]['loudness']
        live = features[0]['liveness']
        speech = features[0]['speechiness']
        tempo = features[0]['tempo']
        valence = features[0]['valence']

    return render_template('home.html', artist=artist, artist_href=artist_href,
                           name=name, song_href=song_href, album=album,
                           album_href=album_href, release_date=release_date,
                           acoustic=acoustic, dance=dance, energy=energy,
                           loud=loud, live=live, speech=speech, tempo=tempo,
                           valence=valence)
