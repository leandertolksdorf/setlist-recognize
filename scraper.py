import requests
import re
from urllib.request import urlretrieve
import html
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

"""
To-Do:
- Mixcloud integration (everything)
"""

class Scraper:

    def __init__ (self, url):
        self.url = url
        # HTML PARSING
        self.html = requests.models.Response
        self.soup = BeautifulSoup
        # METADATA
        self.title = ""
        self.track_id = ""

        
    
    def parse_html (self):
        self.html = requests.get(self.url)
        self.soup = BeautifulSoup(self.html.text, 'html.parser')
    
    @abstractmethod
    def get_track_id (self):
        pass

    @abstractmethod
    def get_title (self):
        pass

    @abstractmethod
    def get_audio (self):
        pass

class Soundcloud(Scraper):

    def __init__(self, url = "https://soundcloud.com/mira_kater/mira-38-katzen-heinz-hopper-kater-blau-291115"):
        super().__init__(url)
        self.headers = {
            'Host': 'api-v2.soundcloud.com',
            'Connection': 'keep-alive',
            'Authorization': 'OAuth 2-290697-105788744-ao7e9JU9hmNo6y',
            'Origin': 'https://soundcloud.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://soundcloud.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'de-DE,de;q=0.9,en-DE;q=0.8,en;q=0.7,en-US;q=0.6'
        }

    def get_track_id (self):
        self.track_id = re.search(r'soundcloud://sounds:(\w+)"', self.html.text).group(1)
    
    def get_title (self):
        self.title = re.split("\ \|", self.soup.title.string)[0]
    
    def get_audio (self, path):

        # GET THE HTTP-REQUEST URL FOR THE MP3 FILE
        metadata = requests.get('https://api.soundcloud.com/tracks/{}'.format(self.track_id), headers=self.headers).json()
        request_mp3 = metadata['media']['transcodings'][1]['url']

        # GET THE FINAL MP3-URL
        mp3_data = requests.get(request_mp3, headers=self.headers).json()
        mp3_url = mp3_data['url']
        
        # DOWNLOAD THE MP3 TO SPECIFIED PATH
        print("Downloading MP3.")
        urlretrieve(mp3_url,"{}/download.mp3".format(path))