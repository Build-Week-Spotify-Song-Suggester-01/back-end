from flask import Flask, render_template, request
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

   
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

token = SpotifyClientCredentials(
    client_id="516dcc7dd59a48eb85604f46f2aa134a",
    client_secret="4326ec02ca5e4df6b46066bb774006a4")
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


def get_audio_features(track_ids, names):
    features = []
    for track in track_ids:
        metrics = sp.audio_features(track)[0]
        features_ = {k : v for k, v in metrics.items()}
        features.append(features_)

    return dict(zip(names, features))


@app.route('/', methods=["POST","GET"])
def home():
    name = request.form.get('song_name')
    artist = ''
    artist_href = ''
    song_name = ''
    song_href = ''
    release_date = ''
    acoustic = None
    dance = None
    energy = None
    live = None
    speech = None
    valence = None
    instrument = None
    titles = []
    artists = []
    ids = []
    track_refs = []
    artist_refs = []
    if name:
        song = sp.search(q=name)
        artist = song['tracks']['items'][0]['album']['artists'][0]['name']
        artist_href = song['tracks']['items'][0]['artists'][0]['external_urls']['spotify']
        song_name = song['tracks']['items'][0]['name']
        song_href = song['tracks']['items'][0]['external_urls']['spotify']
        release_date = song['tracks']['items'][0]['album']['release_date']
        features = sp.audio_features(song_href)
        acoustic = features[0]['acousticness']
        dance = features[0]['danceability']
        energy = features[0]['energy']
        live = features[0]['liveness']
        speech = features[0]['speechiness']
        valence = features[0]['valence']
        instrument = features[0]['instrumentalness']
        ids, titles, artists, track_refs, artist_refs = get_5_recs(name)
    

    return render_template('home.html', artist=artist, artist_href=artist_href,
                           song_name=song_name, song_href=song_href,
                           release_date=release_date, acoustic=acoustic,
                           dance=dance, energy=energy, live=live, speech=speech,
                           valence=valence, titles=titles, artists=artists,
                           track_refs=track_refs, artist_refs=artist_refs,
                           instrument=instrument)
