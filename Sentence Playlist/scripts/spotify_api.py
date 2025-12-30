# -*- coding: utf-8 -*-

import os
import requests
import json
import time
from dotenv import load_dotenv
from pathlib import Path

class APIInteractions:
    """
    Encapsulates all Spotify Web API calls
    """
    
    def search_song(self, word, offset, token):
        """
        Searches Spotify for a track with the same title as the word

        :param word: Track name
        :param offset: Pagination offset for deeper searches
        :param token: Spotify access token
        :return: Spotify track ID or None
        """
        limit = 50
        url = f'https://api.spotify.com/v1/search?q=track%3A{word}&type=track&market=NL&limit={limit}&offset={offset*limit}'
        r = requests.get(url, headers={'Authorization': f'Bearer {token}'})
        self.check_status(r)
        body = r.json()
        items = body['tracks']['items']
        for song in items:
            if song['name'].lower() == word.lower():
                return song['id']
        return None
            
    def create_playlist(self, title, ids, token):
        """
        Creates a Spotify playlist and adds tracks to it

        :param title: Playlist title
        :param ids: List of Spotify track IDs
        :param token: Spotify access token
        """
        load_dotenv()
        user = os.environ.get('SPOTIFY_USER_ID')
        url = f'https://api.spotify.com/v1/users/{user}/playlists'
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        data = {'name': title, "description": "Wijze woorden", "public": False}
        r = requests.post(url, headers=headers, json=data)
        self.check_status(r)
        playlist_id = r.json()['id']
        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        data = {'uris': [f'spotify:track:{item}' for item in ids]}
        r = requests.post(url, headers=headers, json = data)
        self.check_status(r)
        
    def check_status(self, response):
        """
        Raises an exception if the HTTP request failed

        :param response: requests.Response object
        """
        if response.status_code >= 400:
            raise requests.HTTPError(f"{response.status_code} {response.reason}: {response.text}", response=response)
        

class TokenHandling:
    """
    Manages Spotify access tokens and refreshing logic
    """

    def __init__(self, path, api_interactions):
        """
        :param path: Directory containing token.json
        :param api_interactions: APIInteractions instance
        """
        self.token_path = os.path.join(path, 'token.json')
        self.api_interactions = api_interactions
    
    def get_access_token(self):
        """
        Retrieves a valid access token, refreshing it if expired

        :return: Spotify access token
        """
        with open(self.token_path) as f:
            token_file = json.load(f)
        expiry = token_file['expires_at']
        if expiry <= time.time():
            return self.refresh()
        return token_file['access_token']
    
    def refresh(self):
        """
        Refresh the Spotify access token using a refresh token

        :return: New Spotify access token
        """
        load_dotenv()
        credentials = os.environ.get('SPOTIFY_ENCODED_CREDENTIALS')
        refresh_token = os.environ.get('SPOTIFY_REFRESH_TOKEN')
        url = 'https://accounts.spotify.com/api/token'
        headers = {'Authorization': f'Basic {credentials}', 'Content-Type': "application/x-www-form-urlencoded"}
        data = {'grant_type': "refresh_token", 'refresh_token': refresh_token}
        r = requests.post(url, headers=headers, data=data)
        self.api_interactions.check_status(r)
        token_file = r.json()
        token_file['expires_at'] = time.time()+token_file['expires_in']
        with open(self.token_path, 'w') as f:
            json.dump(token_file, f)
        return token_file['access_token']