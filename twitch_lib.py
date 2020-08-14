#Twitch Lib
import requests 
import json 

class TwitchAPI:

    def __init__(self):
        self.headers = {'Client-ID': self.get_client_id(), 'Authorization': f'Bearer {self.get_access_token()}'}

    def get_client_secret(self):
        with open('CLIENT_SECRET.txt', 'r') as f:
            return f.read().strip()
            
    def get_client_id(self):
        with open('CLIENT_ID.txt', 'r') as f:
            return f.read().strip()

    def get_access_token(self):
        access_token = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={self.get_client_id()}&client_secret={self.get_client_secret()}&grant_type=client_credentials")
        return access_token.json()['access_token']

    def make_request(self, URL):
        req = requests.get(URL, headers=self.headers)
        return req.json()
    
    def with_name_get_stream(self, user_name):
        base_url = 'https://api.twitch.tv/helix/streams?user_login='

        URL = base_url + user_name

        return self.make_request(URL)
    
    def with_id_get_stream(self, game_id):
        base_url = 'https://api.twitch.tv/helix/streams?game_id='

        URL = base_url + game_id

        return self.make_request(URL)
    def with_id_get_game(self, game_id):
        base_url = 'https://api.twitch.tv/helix/games?id='

        URL = base_url + game_id

        return self.make_request(URL)
    
    def with_name_get_game(self, game_name):
        base_url = 'https://api.twitch.tv/helix/games?name='

        URL = base_url + game_name
        
        return self.make_request(URL)

    def with_name_get_channel(self, channel_name):
        base_url = 'https://api.twitch.tv/helix/search/channels?query='

        URL = base_url + channel_name

        return self.make_request(URL)