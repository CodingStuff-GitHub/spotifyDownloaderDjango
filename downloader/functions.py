from pprint import pprint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time


def autheticate_client():
    # Authentication
    client_id = 'cff5c45dad994daf8ad2f5bfc9772f77'
    client_secret = 'c34eee877de2435c866d1dd8c5df7657'
    client_credentials_manager = SpotifyClientCredentials(
        client_id, client_secret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_playlist_name_uri(user_id, sp):
    playlist_names_list = []
    playlists_uri_list = []
    playlist_track_number = []
    all_tracks = []
    playlists = sp.user_playlists(user_id)
    while playlists:
        for playlist in playlists['items']:
            playlist_names_list.append(playlist['name'])
            playlists_uri_list.append(
                playlist['uri'].lstrip("spotify:playlist:"))
            playlist_track_number.append(playlist['tracks']['total'])

            ids = []
            tracks = []
            ids = getTrackIDs(user_id, playlist['uri'], sp)
            for id in ids:
                track_features = getTrackFeatures(id, sp)
                tracks.append(track_features)

            all_tracks.append(dict(zip(ids, tracks)))

        playlists = sp.next(playlists) if playlists['next'] else None
    return playlist_names_list, playlists_uri_list, playlist_track_number, all_tracks


def getTrackIDs(user, playlist_id, sp):
    id_list = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        id_list.append(track['id'])
    return id_list


def getTrackFeatures(single_id, sp):
    meta = sp.track(single_id)
    name = meta['name']
    artist = meta['album']['artists'][0]['name']
    album = meta['album']['name']
    return [name, album, artist]
