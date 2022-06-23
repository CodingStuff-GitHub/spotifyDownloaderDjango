from pprint import pprint
from django.shortcuts import render
from . import functions


# Create your views here.


def index(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        sp = functions.autheticate_client()
        user_name = sp.user(user_id).get('display_name')
        playlist_names_list, playlists_uri_list, playlist_track_number, all_tracks = functions.get_playlist_name_uri(
            user_id, sp)
        playlists_zip = list(
            zip(playlist_names_list, playlists_uri_list, playlist_track_number, all_tracks))
    else:
        user_id = ''
        user_name = ''
        playlists_zip = []
    return render(request, 'index.html', {'user_id': user_id, 'user_name': user_name, 'playlists_zip': playlists_zip})


def download(request, val):
    return render(request, 'download.html', {'val': val})
