from .app import sp
import numpy as np


# Grab 5 songs at random from the longest playlist on Spotify
def get_5():
    playlist = sp.playlist_tracks(playlist_id='6yPiKpy7evrwvZodByKvM9',
                                  offset=(np.random.randint(200) * 50),
                                  limit=100)['items']
    track_ids = []
    track_names = []
    track_artists = []
    for num in np.random.choice(100, 5):
        track_ids.append(playlist[num]['track']['id'])
        track_names.append(playlist[num]['track']['name'])
        track_artists.append(playlist[num]['track']['album']['artists'][0]['name'])
    
    return track_ids, track_names, track_artists


def get_audio_features(track_ids):
    features = []
    for track in track_ids:
        features.append(sp.audio_features(track)[0])

    return features

    