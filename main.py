from scraper import Soundcloud
from recognizer import ACRCloud, AudD
from slicer import Slicer
from spotifyapi import SpotifyApi
import tempfile
import time
import json
import os

# class SpotifyApi():
#     def __init__(self, username):
#         self.username = username
#         self.client_id = "c068bdd5c72a43a7acb7fa239835394d"
#         self.client_secret = "ac7b064d36804e2da9693c243ca20163"
#         self.redirect_url = "https://example.com/callback/"
#         self.scope = 'playlist-modify-private,playlist-modify-public'
#         self.token = ""
#         self.api = spotipy.client.Spotify
#         self.playlist_desc = "Created with setlistify."
    
#     def set_username(self, username):
#         self.username = username

#     def get_token(self):
#         try:
#             self.token = util.prompt_for_user_token(self.username,self.scope,client_id=self.client_id,client_secret=self.client_secret,redirect_uri=self.redirect_url)
#             return self.token
        
#         except:
#             os.remove(f".cache={self.username}")
#             self.token = util.prompt_for_user_token(self.username,self.scope,client_id=self.client_id,client_secret=self.client_secret,redirect_uri=self.redirect_url)
#             return self.token
    
#     def open_api(self):
#         self.api = spotipy.Spotify(auth=self.token)
    
#     def create_playlist(self, title, tracks = []):
        
#         playlist = self.api.user_playlist_create(self.username,title)
#         playlist_id = playlist['id']
#         self.api.user_playlist_change_details(self.username,playlist_id,description=self.playlist_desc)

#         if tracks:
#             self.api.user_playlist_add_tracks(self.username,playlist_id,tracks)

# class Slicer():
#     def __init__(self, mp3_file, temp_path):
#         super().__init__()
#         self.mp3_file = mp3_file
#         self.temp_path = temp_path
#         self.density = 60 # seconds
#         self.length = 10 # seconds

#         '''
#         density =   180     | 120   | 60    | 60    | 60    | 120   | 90    | 75    | 75
#         length =    10      | 10    | 15    | 10    | 5     | 5     | 5     | 5     | 10
#         time        1:11    | 1:55  | 3:39  | 3:29  | 3:23  | 1:47  | 2:20  | 2:48  | 2:42
#         tracks      14      | 16    | 20    | 20    | 20    | 16    | 18    | 19    | 19
#         '''

#     def set_density(self,density):
#         self.density = density

#     def set_length(self,length):
#         self.length = length

#     def make_samples(self):

#         # Make folders

#         os.mkdir('{}/samples'.format(self.temp_path))

#         # Slice mp3 into segments of set density. Save slices in temporary directory.

#         slices = tempfile.TemporaryDirectory(dir = self.temp_path)

#         subprocess.run(['ffmpeg', '-i',str(self.mp3_file), '-f','segment', '-segment_time', str(self.density), '-c', 'copy', '{}/slice_%03d.mp3'.format(slices.name)])

#         # Trim slices to set length.

#         sample_number = 0

#         for filename in os.listdir("{}".format(slices.name)):
#             subprocess.run(['ffmpeg','-i','{}/{}'.format(slices.name,filename),'-ss','0','-to',str(self.length),'-c','copy','-y','{}/samples/sample_{}.mp3'.format(self.temp_path,sample_number)])

#             sample_number += 1
        
# class Recogniser():
#     def __init__(self,samples_path = "samples"):
#         self.samples_path = samples_path
#         self.config = {
#             'host':'identify-eu-west-1.acrcloud.com',
#             'access_key':'44ca71ee7e16be0608b6db4f9195ae71', 
#             'access_secret':'HATkSNXtKQKDxlYXNqAWaBgkknZGr1hGjhIFWQXG',
#             'timeout':10 # seconds
#         }
#         self.api = ACRCloudRecognizer(self.config)
#         self.results = []
#         self.spotify_ids = []
    
#     def get_results(self):
#         results = []
#         for sample in os.listdir(self.samples_path):
#             result = self.api.recognize_by_file("{}/{}".format(self.samples_path,sample),0)
#             print(result)
#             if result not in results:
#                 results.append(json.loads(result))
#         self.results = results
#         return self.results
    
#     def get_spotify(self):
#         spotify_ids = []

#         for elem in self.results:
#             try:
#                 spotify_id = elem['metadata']['music'][0]['external_metadata']['spotify']['track']['id']
#                 if spotify_id not in spotify_ids:
#                     spotify_ids.append(spotify_id)
#             except:
#                 pass
#         self.spotify_ids = list(filter(lambda x: x != None, spotify_ids))
#         print("Found " , len(self.spotify_ids) , " Spotify-IDs.")
    
#     def get_deezer(self):
#         deezer_ids = []

#         for elem in self.results:
#             try:
#                 deezer_id = elem['metadata']['music'][0]['external_metadata']['deezer']['track']['id']
#                 if deezer_id not in deezer_ids:
#                     deezer_ids.append(deezer_id)
#             except:
#                 pass
#         self.deezer_ids = list(filter(lambda x: x != None, deezer_ids))
#         print("Found " , len(deezer_ids) , " Deezer-IDs.")

# def download_track(url,path):

#     HEADERS = {
#         'Host': 'api-v2.soundcloud.com',
#         'Connection': 'keep-alive',
#         'Authorization': 'OAuth 2-290697-105788744-ao7e9JU9hmNo6y',
#         'Origin': 'https://soundcloud.com',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
#         'Accept': '*/*',
#         'Sec-Fetch-Site': 'same-site',
#         'Sec-Fetch-Mode': 'cors',
#         'Referer': 'https://soundcloud.com/',
#         'Accept-Encoding': 'gzip, deflate, br',
#         'Accept-Language': 'de-DE,de;q=0.9,en-DE;q=0.8,en;q=0.7,en-US;q=0.6'
#     }

#     # GET THE HTML
#     html = requests.get(url)

#     # GET THE TRACK ID
#     track_id = re.search(r'soundcloud://sounds:(\w+)"', html.text).group(1)
#     #print("Track-ID: " + track_id)

#     # GET THE HTTP-REQUEST URL FOR THE MP3 FILE
#     metadata = requests.get('https://api.soundcloud.com/tracks/{}'.format(track_id), headers=HEADERS).json()
#     request_mp3 = metadata['media']['transcodings'][1]['url']
#     #print("MP3 Link request: " + request_mp3)

#     # GET THE FINAL MP3-URL
#     mp3_data = requests.get(request_mp3, headers=HEADERS).json()
#     mp3_url = mp3_data['url']
#     #print("MP3-URL: " + mp3_url)
    
#     # DOWNLOAD THE MP3 TO SPECIFIED PATH
#     print("Downloading MP3.")
#     urlretrieve(mp3_url,"{}/download.mp3".format(path))

def main():

    dump_path = "dumps"

    # CREATE TEMP. DIRECTORY AND SAMPLE DIRECTORY
    temp = tempfile.TemporaryDirectory(dir = "")
    sample_path = "{}/samples".format(temp.name)

    # GET USER INPUT & ESTABLISH SPOTIFY API CONNECTION
    print("--- SETLISTIFY ---")
    username = input("Enter username: ")

    spotify = SpotifyApi(username)
    spotify.get_token()

    url = input("Enter URL here: ")

    start_time = time.time()

    # CHECK FOR SOURCE

    if "soundcloud" in url:
        scraper = Soundcloud(url)
        source = "soundcloud"
    elif "mixcloud" in url:
        source = "mixcloud"
        pass
    else:
        print("Not a valid URL.")
    
    # GET TRACK ID

    scraper.parse_html()
    scraper.get_track_id()
    scraper.get_title()

    dump_filename = "{1}_{2}.json".format(dump_path, source, scraper.track_id)

    # CHECK IF ALREADY PROCESSED

    if dump_filename in os.listdir("dumps"):
        print("Already processed " + scraper.title)
        return


    scraper.get_audio(temp.name)

    # Downloaded mp3 is now in temp-dir.

    # SLICE MP3

    slicer = Slicer("{}/download.mp3".format(temp.name), temp.name)
    slicer.make_samples()

    # RECOGNISE

    results = []

    recognizer = ACRCloud("{}/samples".format(temp.name))
    #recognizer = AudD("{}/samples".format(temp.name))


    recognizer.get_results()
    recognizer.get_spotify()
    recognizer.get_deezer()

    # DUMP DATA TO A JSON-FILE

    dump = {"source":   source,
            "url":      url,
            "track_id": scraper.track_id,
            "title":    scraper.title,
            "recognizer": recognizer.__class__.__name__,
            "results":  recognizer.results
    }

    with open("{0}/{1}".format(dump_path, dump_filename), "w") as json_file:
        json.dump(dump, json_file, indent = 4)


    # MAKE PLAYLIST

    spotify.open_api()
    spotify.create_playlist(scraper.title ,recognizer.spotify_ids)

    end_time = time.time()

    print("Finished in ", (end_time-start_time))

