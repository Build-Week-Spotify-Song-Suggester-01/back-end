# Imports
from flask import Flask, render_template, request
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os

# Making and configuring flask app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

# creating token to get into Spotify API
token = SpotifyClientCredentials(
    client_id="516dcc7dd59a48eb85604f46f2aa134a",
    client_secret="4326ec02ca5e4df6b46066bb774006a4")
# connecting token to spotipy for data extraction
sp = spotipy.Spotify(auth_manager=token)


def get_5_recs(song_name):
    song = sp.search(q=song_name)
    song_id = song['tracks']['items'][0]['id']
    song_name = song['tracks']['items'][0]['name']
    song_artist = song['tracks']['items'][0]['album']['artists'][0]['name']
    recs = sp.recommendations(seed_tracks=[str(song_id)],
                              limit=5)['tracks']
    track_ids = []
    track_titles = []
    track_artists = []
    track_refs = []
    artist_refs = []
    for rec in recs:
        track_ids.append(rec['id'])
        track_titles.append(rec['name'])
        track_artists.append(rec['album']['artists'][0]['name'])
        track_refs.append(rec['external_urls']['spotify'])
        artist_refs.append(rec['album']['artists'][0]['external_urls']['spotify'])
    
    return track_ids, track_titles, track_artists, track_refs, artist_refs


# Home route
@app.route('/', methods=["POST","GET"])
def home():
    """ Getting song name and returning song and
    audio feature metrics """
    name = request.form.get('song_name')
    artist = ''
    artist_href = ''
    song_name = ''
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
    titles = []
    artists = []
    ids = []
    track_refs = []
    artist_refs = []
    if name:
        song = sp.search(q=name)
        artist = song['tracks']['items'][0]['album']['artists'][0]['name']
        artist_href = song['tracks']['items'][0]['artists']\
            [0]['external_urls']['spotify']
        artist_href = song['tracks']['items'][0]['artists'][0]['external_urls']['spotify']
        song_name = song['tracks']['items'][0]['name']
        song_href = song['tracks']['items'][0]['external_urls']['spotify']
        album = song['tracks']['items'][0]['album']['name']
        album_href = song['tracks']['items'][0]['album']\
            ['external_urls']['spotify']
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
        ids, titles, artists, track_refs, artist_refs = get_5_recs(name)


    return render_template('home.html', artist=artist, artist_href=artist_href,
                           song_name=song_name, song_href=song_href, album=album,
                           album_href=album_href, release_date=release_date,
                           acoustic=acoustic, dance=dance, energy=energy,
                           loud=loud, live=live, speech=speech, tempo=tempo,
                           valence=valence, titles=titles, artists=artists,
                           track_refs=track_refs, artist_refs=artist_refs)
