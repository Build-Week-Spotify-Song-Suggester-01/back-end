# import statements
from flask import Flask, render_template, request
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import matplotlib.pyplot as plt
import numpy as np

# making and configuring flask app
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['EXPLAIN_TEMPLATE_LOADING'] = True

# token for Spotify API
token = SpotifyClientCredentials(
    client_id="516dcc7dd59a48eb85604f46f2aa134a",
    client_secret="4326ec02ca5e4df6b46066bb774006a4")
# connecting to Spotipy using token
sp = spotipy.Spotify(auth_manager=token)


def get_5_recs(song_name):
    """ Function to use .recommendations() to
    return 5 similar songs """
    song = sp.search(q=song_name)
    song_id = song['tracks']['items'][0]['id']
    song_name = song['tracks']['items'][0]['name']
    song_artist = song['tracks']['items'][0]['album']['artists'][0]['name']
    # .recommendations returns 5 similar songs
    recs = sp.recommendations(seed_tracks=[str(song_id)],
                              limit=5)['tracks']
    track_ids = []
    track_titles = []
    track_artists = []
    track_refs = []
    artist_refs = []
    # for loop to return track id, title, artist and the url
    # for song recommendations
    for rec in recs:
        track_ids.append(rec['id'])
        track_titles.append(rec['name'])
        track_artists.append(rec['album']['artists'][0]['name'])
        track_refs.append(rec['external_urls']['spotify'])
        artist_refs.append(
            rec['album']['artists'][0]['external_urls']['spotify'])

    return track_ids, track_titles, track_artists, track_refs, artist_refs


def get_audio_features(track_ids, names):
    """ Function to get audio features and return
    as a dictionary """
    features = []
    for track in track_ids:
        metrics = sp.audio_features(track)[0]
        features_ = {k: v for k, v in metrics.items()}
        features.append(features_)

    return dict(zip(names, features))

def make_graphs(song):
    '''makes 6 bar graphs displaying the audio features of
    the input song and the 5 suggested songs'''
    # get recommended songs
    ids, names, artists, t_refs, a_refs = get_5_recs(song)

    # get audio features of recommended songs
    features = []
    for track in ids:
        features.append(sp.audio_features(track)[0])

    # get features for original song
    original_song = sp.search(q=song)
    song_id = original_song['tracks']['items'][0]['id']
    original_features = sp.audio_features(song_id)

    # binary features are between 0 and 1
    binary_feats = ['danceability', 'energy', 'speechiness', 'acousticness',
                    'instrumentalness', 'liveness', 'valence']

    # other features are not between 0 and 1 but still numeric
    other_feats = ['mode', 'time_signature', 'tempo',
                   'duration_ms', 'loudness']

    # get binary feature values for original song
    binary_vals = []
    for feat in binary_feats:
        binary_vals.append(original_features[0][feat])

    # create subplots
    fig, ax = plt.subplots(6, 1, sharex='col', sharey='col', figsize=(6, 8))
    # configure subplots
    plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9,
                        top=1.5, wspace=0.2, hspace=0.5)

    # plot the original song's metrics
    y_pos = np.arange(len(binary_feats))
    ax[0].barh(y_pos, binary_vals, align='center',
               color=['b', 'm', 'g', 'b', 'tab:orange', 'y', 'r'],
               edgecolor='k', linewidth=1)

    # set up rest of graph
    ax[0].set_yticks(y_pos)
    ax[0].set_yticklabels(binary_feats)
    ax[0].invert_yaxis()  # labels read top-to-bottom
    ax[0].set_xlabel('Rating')
    ax[0].set_title('Original Song Metrics')

    # loop through each suggested song
    for i in range(len(ids)):
        # get audio features for each song
        binary_vals = []
        for feat in binary_feats:
            binary_vals.append(features[i][feat])

        # plot each song and label the x-axis and title
        ax[i+1].barh(y_pos, binary_vals, align='center',
                     color=['b', 'm', 'g', 'b', 'tab:orange', 'y', 'r'],
                     edgecolor='k', linewidth=1)
        ax[i+1].set_xlabel('Rating')
        ax[i+1].set_title(f'Suggested Song {i+1} Metrics')

    plt.show()


@app.route('/', methods=["POST", "GET"])
def home():
    """ Home function to return song and audio metrics """
    # getting song and assigning to "name"
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
        artist_href = song['tracks']['items'][0]['artists'][0]\
            ['external_urls']['spotify']
        song_name = song['tracks']['items'][0]['name']
        song_href = song['tracks']['items'][0]['external_urls']['spotify']
        release_date = song['tracks']['items'][0]['album']['release_date']
        # assigning song metrics to "features"
        features = sp.audio_features(song_href)
        acoustic = features[0]['acousticness']
        dance = features[0]['danceability']
        energy = features[0]['energy']
        live = features[0]['liveness']
        speech = features[0]['speechiness']
        valence = features[0]['valence']
        instrument = features[0]['instrumentalness']
        ids, titles, artists, track_refs, artist_refs = get_5_recs(name)

    # retuning the template for html encoding
    return render_template('home.html', artist=artist, artist_href=artist_href,
                           song_name=song_name, song_href=song_href,
                           release_date=release_date, acoustic=acoustic,
                           dance=dance, energy=energy, live=live,
                           speech=speech, valence=valence, titles=titles,
                           artists=artists, track_refs=track_refs,
                           artist_refs=artist_refs, instrument=instrument)
