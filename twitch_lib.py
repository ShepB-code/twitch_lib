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
    
    def get_user_stream(self, user_name):
        user_stream_url = 'https://api.twitch.tv/helix/streams?user_login='

        URL = user_stream_url + user_name

        return self.make_request(URL)

    def get_game(self, game_id):
        game_url = 'https://api.twitch.tv/helix/games?id='

        URL = game_url + game_id

        return self.make_request(URL)

    def get_channel(self, channel_name):
        search_channel_url = 'https://api.twitch.tv/helix/search/channels?query='

        URL = search_channel_url + channel_name

        return self.make_request(URL)