import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

### This module handles authentication with the Spotify API using the spotipy library.

def get_spotify_client():
    # load environment variables from .env file
    load_dotenv()

    client_id, client_secret, redirect_uri, soundnet_api_key = (
        os.getenv("SPOTIFY_CLIENT_ID"),
        os.getenv("SPOTIFY_CLIENT_SECRET"),
        os.getenv("SPOTIFY_REDIRECT_URI"),
        os.getenv("SOUNDNET_API_KEY")
    )

    # authenticate with Spotify using the spotipy library
    local_auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-library-read playlist-read-private playlist-read-collaborative",
    )

    spotify_instance = Spotify(auth_manager=local_auth_manager)

    return spotify_instance

