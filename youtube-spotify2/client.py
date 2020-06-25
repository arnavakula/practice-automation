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
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class MainApp():

    def __init__(self):
        self.user_id = info.spotify_id
        self.oauth = info.spotify_oauth
        self.playlist_name = info.spotify_playlist
        self.youtube_client = self.get_youtube_client()

    def get_youtube_client(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secret.json"

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
        credentials = flow.run_console()

        youtube_client = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

        return youtube_client

    def get_liked_songs(self):
        pass

    def get_playlist_id(self):
        url = 'https://api.spotify.com/v1/users/{}/playlists'.format(self.user_id)

        response = requests.get(
            url, 
            headers = {
                'Authorization': 'Bearer {}'.format(self.oauth)
            }
        )

        names = [pl['name'] for pl in response.json()['items']]
        ids = [pl['id'] for pl in response.json()['items']]

        if not self.playlist_name in names:
            request_body = json.dumps({
                'name': '{}'.format(self.playlist_name),
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

        try:
            return ids[names.index(self.playlist_name)]
        except ValueError:
            print('Sorry, there was an error in initializing the playlist. Try reauthenticating your oauth token')

    def get_song_id(self, artist, track):
        search_url = 'https://api.spotify.com/v1/search?q={}%20{}&type=track'.format(artist, track)

        response = requests.get(
            search_url,
            headers = {
                'Content-Type': 'applications/json',
                'Authorization': 'Bearer {}'.format(self.oauth)
            }
        )

        response_json = response.json()

        return response_json['tracks']['items'][0]['id']

    def add_song(self, song_id):
        url = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(self.user_id, self.get_playlist_id())
        print(url)

        print('spotify:track:{}'.format(song_id))

        request_body = {
            'uris':['spotify:track:{}'.format(song_id)]
        }
        
        response = requests.post(
            url, 
            data = request_body,
            headers = {
                'Content-Type': 'applications/json',
                'Authorization': 'Bearer {}'.format(self.oauth)
            }
        )
   
            
       
        



app = MainApp()
# app.get_playlist_id()
# song_id = app.get_song_id('drake', 'jumpman')
# app.add_song(song_id)

