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
import youtube_dl

class MainApp():

    def __init__(self):
        self.user_id = info.spotify_id
        self.oauth = info.spotify_oauth
        self.playlist_name = info.spotify_playlist
        self.song_info = {} #dict where values are a bio-dict
        # self.youtube_client = self.get_youtube_client()

    def get_youtube_client(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secrets.json"

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
        
        credentials = flow.run_local_server()

        youtube_client = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

        return youtube_client

    def store_liked_songs(self):
        request = self.youtube_client.videos().list(
            part = 'snippet, contentDetails, statistics',
            myRating = 'like'
        )

        response = request.execute()
        
        for item in response['items']:
            title = item['snippet']['title']
            url = 'https://www.youtube.com/watch?v={}'.format(item['id'])

            bio = youtube_dl.YoutubeDL().extract_info(url, download=False)
            track = bio['track']
            artist = bio['artist']

            self.song_info[title] = {
                'url': url,
                'track': track,
                'artist': artist
            }

            print(self.song_info)

    def create_playlist(self):
        url = 'https://api.spotify.com/v1/users/{}/playlists'.format(self.user_id)

        response = requests.get(
            url,
            headers = {
                'Authorization': 'Bearer {}'.format(self.oauth)
            }
        )

        response_json = response.json()
        pl_names = [pl['name'] for pl in response_json['items']]

        if not self.playlist_name in pl_names:
            request_body = json.dumps({
                'name': '{}'.format(self.playlist_name),
                'description': 'Automated from Youtube',
                'public': False
            })

            response2 = requests.post(
                url, 
                data = request_body,
                headers = {
                    'Content-Type': 'applications.json',
                    'Authorization': 'Bearer {}'.format(self.oauth)
                }
            )
        else:
            print('You already have a playlist for this app.')

    def get_playlist_id(self):
        url = 'https://api.spotify.com/v1/users/{}/playlists'.format(self.user_id)

        response = requests.get(
            url,
            headers = {
                'Authorization': 'Bearer {}'.format(self.oauth)
            }
        )

        response_json = response.json()
        pl_names = [pl['name'] for pl in response_json['items']]
        pl_ids = [pl['id'] for pl in response_json['items']]

        return pl_ids[pl_names.index(self.playlist_name)]

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
# print(app.get_song_id(('drake'), ('jumpman')))
print(app.get_playlist_id())


# lst = [{'artist': 'Lil Mosey', 'track': 'Blueberry Faygo'}, {'artist': '24kGoldn', 'track': 'Valentino'}, {'artist': 'Roddy Ricch', 'track': 'High Fashion'}]
# print(lst[0]['artist'])
