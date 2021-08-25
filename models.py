from .app import sp
import numpy as np


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
    for rec in recs:
        track_ids.append(rec['id'])
        track_titles.append(rec['name'])
        track_artists.append(rec['album']['artists'][0]['name'])
    
    return track_ids, track_titles, track_artists


def get_audio_features(track_ids):
    features = []
    for track in track_ids:
        features.append(sp.audio_features(track)[0])

    return features

    