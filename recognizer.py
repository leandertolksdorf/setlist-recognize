from acrcloud.recognizer import ACRCloudRecognizer
import os
import json
import requests
import asyncio
import websockets
from abc import ABC, abstractmethod


class Recognizer():
    def __init__(self,samples_path = "samples"):
        self.samples_path = samples_path
        self.results = []
        self.spotify_ids = []
        self.deezer_ids = []
        self.apple_music_ids = []

    @abstractmethod
    def get_results(self):
        pass
    
    def save_results(self, filename):
        for result in self.results:
            with open((filename + ".json"), "w") as write_file:
                json.dump(result, write_file)
    
    @abstractmethod
    def get_spotify(self):
        pass

    @abstractmethod
    def get_deezer(self):
        pass

class AudD(Recognizer):
    def __init__(self, samples_path):
        super().__init__(samples_path)
        self.token = "69f5c3fcfc8b49173fe4874b46f94ca9"
        self.wss = "wss://api.audd.io/ws/?api_token=" + self.token
        self.api = "https://api.audd.io/"
        self.data = {
                    'return': 'apple_music,deezer,spotify',
                    'api_token': self.token
        }

    def get_results(self):
        null = None # for testing (bc the ["result"] of a failed recognition is null.)

        results = []
        samples = os.listdir(self.samples_path)
        samples.sort()
        for sample in samples:
            with open("{0}/{1}".format(self.samples_path, sample), 'rb') as file:
                result = requests.post(self.api, data=self.data, files={'file': file})
                result = result.json()
                if (result["result"] == None):
                    print("No Track found.")

                elif (result in results):
                    print("Found duplicate: " + result["result"]["artist"] + " - " + result["result"]["title"])

                else:
                    print("Found Track: " + result["result"]["artist"] + " - " + result["result"]["title"])
                    results.append(result)
                
        self.results = results

    def get_spotify(self):

        spotify_ids = []

        for result in self.results:
            try:
                spotify_id = result["result"]["spotify"]["id"]
                spotify_ids.append(spotify_id)
            except:
                print("No Spotify-ID found.")
        
        print("Found " , len(spotify_ids) , " Spotify-IDs")
        
        self.spotify_ids = spotify_ids

    def get_deezer(self):

        deezer_ids = []

        for result in self.results:
            try:
                deezer_id = result["deezer"]["id"]
                deezer_ids.append(deezer_id)
            except:
                print("No Deezer-ID found.")
        
        print("Found " , len(deezer_ids) , " Deezer-IDs")
        
        self.deezer_ids = deezer_ids
    
    def get_apple_music(self):
        apple_music_ids = []

        for result in self.results:
            try:
                apple_music_id = result["apple_music"]["id"]
                apple_music_ids.append(apple_music_id)
            except:
                print("No Apple Music-ID found")
        
        print("Found " , len(apple_music_ids), " Apple Music-IDs")
        self.apple_music_ids = apple_music_ids
            




class ACRCloud(Recognizer):
    def __init__(self, samples_path):
        super().__init__(samples_path)
        self.config = {
            'host':'identify-eu-west-1.acrcloud.com',
            'access_key':'44ca71ee7e16be0608b6db4f9195ae71', 
            'access_secret':'HATkSNXtKQKDxlYXNqAWaBgkknZGr1hGjhIFWQXG',
            'timeout':10 # seconds
        }
        self.api = ACRCloudRecognizer(self.config)

    def get_results(self):
        results = []
        samples = os.listdir(self.samples_path)
        samples.sort()
        for sample in samples:
            result = json.loads(self.api.recognize_by_file("{}/{}".format(self.samples_path,sample),0))
            print(sample)
            if (result not in results) & (result["status"]["code"] == 0):
                print(result)
                results.append(result)
        self.results = results
        print("Found ", len(self.results), " results.")
        return self.results
    
    def get_spotify(self):
        spotify_ids = []

        for elem in self.results:
            try:
                spotify_id = elem['metadata']['music'][0]['external_metadata']['spotify']['track']['id']
                if spotify_id not in spotify_ids:
                    spotify_ids.append(spotify_id)
            except:
                pass
        self.spotify_ids = list(filter(lambda x: x != None, spotify_ids))
        print("Found " , len(self.spotify_ids) , " Spotify-IDs.")
    
    def get_deezer(self):
        deezer_ids = []

        for elem in self.results:
            try:
                deezer_id = elem['metadata']['music'][0]['external_metadata']['deezer']['track']['id']
                if deezer_id not in deezer_ids:
                    deezer_ids.append(deezer_id)
            except:
                pass
        self.deezer_ids = list(filter(lambda x: x != None, deezer_ids))
        print("Found " , len(deezer_ids) , " Deezer-IDs.")

    