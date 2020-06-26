from youtube_client import YoutubeClient
from spotify_client import SpotifyClient

def run():
    youtube_client = YoutubeClient('client_secret.json')
    spotify_client = SpotifyClient('BQCZQpa6N1lnjZtdNdkSZpG-Vwxk4zAwXG_DLGN2rOa_D6Ddq7_S6jdUOwalI2J_rU4IUaZwgZ-dVrGLfEKT1_L2WsyVR6PieIxcgOBkD1OFAE6J7OeMk-mXGKdH5Njww__7eA8lkfKDZAAV7OSRjg')
    playlists = youtube_client.get_playlists()

    for index, playlist in enumerate(playlists):
        print(f'{index}: {playlist.title}')

    choice = int(input('Enter a corresponding number: '))
    chosen = playlists[choice]
    print(f'You selected {chosen.title}')

    songs = youtube_client.get_videos(chosen.id)
    print(f'Attempting to read {len(songs)}')

    for song in songs:
        sid = spotify_client.search_song(song.artist, song.track)

        if sid:
            added_song = spotify_client.add_song(sid)

            if added_song():
                print('Successful')



if __name__ == '__main__':
    run()   