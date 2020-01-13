import spotipy
import spotipy.util as util
import os

class SpotifyApi():
    def __init__(self, username = "leanderto1"):
        self.username = username
        self.client_id = "c068bdd5c72a43a7acb7fa239835394d"
        self.client_secret = "ac7b064d36804e2da9693c243ca20163"
        self.redirect_url = "https://example.com/callback/"
        self.scope = 'playlist-modify-private,playlist-modify-public'
        self.token = ""
        self.api = spotipy.client.Spotify
        self.playlist_desc = "Created with setlistify."
    
    def set_username(self, username):
        self.username = username

    def get_token(self):
        try:
            self.token = util.prompt_for_user_token(self.username,self.scope,client_id=self.client_id,client_secret=self.client_secret,redirect_uri=self.redirect_url)
            return self.token
        
        except:
            os.remove(f".cache={self.username}")
            self.token = util.prompt_for_user_token(self.username,self.scope,client_id=self.client_id,client_secret=self.client_secret,redirect_uri=self.redirect_url)
            return self.token
    
    def open_api(self):
        self.api = spotipy.Spotify(auth=self.token)
    
    def create_playlist(self, title, tracks = []):
        
        playlist = self.api.user_playlist_create(self.username,title)
        playlist_id = playlist['id']
        self.api.user_playlist_change_details(self.username,playlist_id,description=self.playlist_desc)

        if tracks:
            self.api.user_playlist_add_tracks(self.username,playlist_id,tracks)