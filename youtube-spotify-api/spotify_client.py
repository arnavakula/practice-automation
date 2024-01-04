import requests
import urllib.parse
from security import safe_requests

class SpotifyClient(object):
    def __init__(self, oauth):
        self.oauth = oauth

    def search_song(self, artist, track):
        query = urllib.parse.quote(f'{artist} {track}')
        url = f'https://api.spotify.com/v1/search?q={query}&type=track'
        response = safe_requests.get(url,
            headers = {
                'Content-Type': 'applications/json',
                'Authorization': f'Bearer {self.oauth}'
            } 
        )

        rjson = response.json()
        results = rjson['tracks']['items']

        if results:
            return results[0]['id']
        else:
            raise Exception(f'No search result')

    def add_song(self, id):
        url = 'https://api.spotify.com/v1/me/tracks'
        response = requests.put(
            url,
            json = {
                'ids': [id]
            },
            headers = {
                'Content-Type': 'applications/json',
                'Authorization': f'Bearer {self.oauth}'
            }
        )

        return response.ok()

