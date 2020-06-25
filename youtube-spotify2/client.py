'''
manual steps:
login to youtube
check liked videos
get song names
search spotify
create playlist
add song to playlist
'''

import json
import requests
import info

class MainApp():

    def __init__(self):
        self.user_id = info.spotify_id
        self.oauth = info.spotify_oauth
        self.playlist_name = info.spotify_playlist

    def get_youtube_client(self):
        pass

    def get_liked_songs(self):
        pass

    def create_playlist(self):
        url = 'https://api.spotify.com/v1/users/{}/playlists'.format(self.user_id)

        response = requests.get(
            url, 
            headers = {
                'Authorization': 'Bearer {}'.format(self.oauth)
            }
        )

        playlists = [playlist['name'] for playlist in response.json()['items']]

        if not self.playlist_name in playlists:
            request_body = json.dumps({
                'name': '{}'.format(playlist_name),
                'description': 'Automated from Youtube',
                'public': False
            })

            response = requests.post(
                url, 
                data = request_body,
                headers = {
                    'Content-Type': 'applications/json',
                    'Authorization': 'Bearer {}'.format(self.oauth)
                }
            )
    
    def get_spotify_id(self, artist, name):
        search_url = 'https://api.spotify.com/v1/search?q={}%20{}&type=track'.format(artist, name)

        response = requests.get(
            search_url,
            headers = {
                'Content-Type': 'applications/json',
                'Authorization': 'Bearer {}'.format(self.oauth)
            }
        )

        response_json = response.json()

        return response_json['tracks']['items'][0]['id']


    def add_song(self, playlist_id = '11StXAlX9HSeUwDBuBj8xs', song_id = '4wVOKKEHUJxHCFFNUWDn0B?si=opGFD9Z9Qn2OuttMLE9nWw'):
        url = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)

        query = json.dumps({
            'uris': 'spotify:track:{}'.format(song_id)
        })

        response = requests.post(
            url, 
            data = query,
            headers = {
                'Content-Type': 'applications/json',
                'Authorization': 'Bearer {}'.format(self.oauth)
            }
        )

        



app = MainApp()
app.create_playlist()

