import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import urllib.request
import re
from pytube import YouTube
import os

# Authentication
client_id = 'cff5c45dad994daf8ad2f5bfc9772f77'  # Add your own client_id
client_secret = 'c34eee877de2435c866d1dd8c5df7657'  # Add your own client secret
user_id = 'in3129p3027fv7yt8ls1knrxi'  # Add user id
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def getTrackIDs(user, playlist_id):
    id_list = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        id_list.append(track['id'])
    return id_list


def getTrackFeatures(single_id):
    meta = sp.track(single_id)
    name = meta['name']
    artist = meta['album']['artists'][0]['name']
    album = meta['album']['name']
    return [name, album, artist]


if __name__ == '__main__':
    playlists_uri_list = []
    playlist_names_list = []
    playlist_artists_list = []
    playlists = sp.user_playlists(user_id)
    while playlists:
        for playlist in playlists['items']:
            playlist_names_list.append(playlist['name'])
            playlists_uri_list.append(
                playlist['uri'].lstrip("spotify:playlist:"))
        playlists = sp.next(playlists) if playlists['next'] else None
    print("Playlist of the user_id given : ")
    print(playlist_names_list)

    try:
        os.mkdir("Downloaded Music")
    except FileExistsError:
        print("Downloaded Music Folder exists")
    
    # Tracks of all the playlists and number of tracks in the playlist
    for i in range(len(playlists_uri_list)):
        current_playlist = playlists_uri_list[i]
        current_playlist_name = playlist_names_list[i]
        try:
            os.mkdir(f"Downloaded Music/{current_playlist_name}")
        except FileExistsError:
            print("Folder Already exists")
        ids = getTrackIDs(user_id, current_playlist)
        print(
            f"\nNumber of tracks in the playlist '{current_playlist_name}' : {len(ids)}")
        print("Starting Downloading .................")

        # loop over track ids
        tracks = []
        for j in range(len(ids)):
            time.sleep(.5)
            track = getTrackFeatures(ids[j])
            tracks.append(track)

        for index, track in enumerate(tracks, start=1):
            song_name = track[0]
            artist_name = track[1]
            album_name = track[2]
            search_terms = f'{song_name} {artist_name} {album_name} Audio'
            print(f"{str(index)}. {search_terms}")

            html = urllib.request.urlopen(
                "https://www.youtube.com/results?search_query=" + re.sub(r'[^a-zA-Z0-9\s]', '+', search_terms).replace(
                    ' ', '+'))
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            youtube_link = f"https://www.youtube.com/watch?v={video_ids[0]}"
            # url input from user
            yt = YouTube(youtube_link)
            # extract only audio
            video = yt.streams.filter(only_audio=True).first()
            # download the file
            out_file = video.download(
                output_path=f"Downloaded Music/{current_playlist_name}")

            # save the file
            base, ext = os.path.splitext(out_file)
            new_file = f'{base}.mp3'
            try:
                os.rename(out_file, new_file)
            except FileExistsError:
                print("File already exists")
            # result of success
            print(f"{yt.title} has been successfully downloaded.")
