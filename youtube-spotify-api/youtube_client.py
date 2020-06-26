import os

import google_auth_oauthlib
import googleapiclient.discovery 
import youtube_dl

class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title

class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track

class YoutubeClient(object):

    def __init__(self, creds_location):
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            creds_location, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)
        
        self.youtube_client = youtube_client


    def get_playlists(self):
        request = self.youtube_client.playlist().list(
            part = 'id, snippet',
            maxResults = 50,
            mine = True
        )

        response = request.execute()
        playlists = [Playlist(pl['id'], pl['snippet']['title']) for pl in response['items']]

        return playlists

    def get_videos(self, pid):
        songs = []
        request = self.youtube_client.playlist().list(
            part = 'id, snippet',
            maxResults = 50,
            mine = True
        )

        response = request.execute()

        for item in response['items']:
            vid = item['snippet']['resourceId']['videoId']
            artist, track = self.get_artist_and_track(vid)
            if artist and track:
                songs.append(Song(artist, track))
            
    def get_artist_and_track(self, vid):
        url = f'https://youtube.com/watch?v={vid}'
        video = youtube_dl.YoutubeDL({'quiet': True, }).extract_info(
            url, download = False
        )

        artist = video['artist']
        track = video['track']

        return artist, track
