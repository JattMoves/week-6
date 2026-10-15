# your code here ...
import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class Genius:
    def __init__(self, access_token=None):
        """Initialize the access token for the Genius API"""
        self.access_token = access_token or os.getenv("ACCESS_TOKEN")
        if not self.access_token:
            raise ValueError("ACCESS_TOKEN is missing from the .env file.")
 

    def get_access_token(self):
        """Return the stored Genius API access token"""
        return self.access_token
    
    def get_artist(self, search_term): 
        """Get artist information by search term."""
        response = requests.get(
            "https://api.genius.com/search",
            params={"q": search_term},
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response.raise_for_status()

        hits = response.json()["response"]["hits"]
        artist_id = hits[0]["result"]["primary_artist"]["id"]

        response = requests.get(
            f"https://api.genius.com/artists/{artist_id}",
            headers={"Authorization": f"Bearer {self.access_token}"}
        )
        response.raise_for_status()

        return response.json()


    def get_artists(self, search_terms):
        """Get information for multiple artists by their search terms."""
        rows = []
        for term in search_terms:
            artist = artist = self.get_artist(term)["response"]["artist"]
            rows.append({
                "search_term": term,
                "artist_name": artist["name"],
                "artist_id": artist["id"],
                "followers_count": artist.get("followers_count")
            })

        return pd.DataFrame(rows)