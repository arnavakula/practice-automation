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

    def get_youtube_client(self):
        pass

    def get_liked_songs(self):
        pass

    def search_spotify(self):
        pass

    def create_playlist(self):
        url = 'https://api.spotify.com/v1/users/{}/playlists'.format(self.user_id)

        request_body = json.dumps({
            'name': 'Liked songs',
            'description': 'Automated from Youtube',
            'public': False
        })

        print('got here')

        response = requests.post(
            url, 
            data = request_body,
            headers = {
                'Content-Type': 'applications/json',
                'Authorization': 'Bearer {}'.format(self.oauth)
            }
        )

app = MainApp()

app.create_playlist()


