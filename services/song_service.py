import os

import httpx
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

LRCLIB_API_BASE_URL = "https://lrclib.net/api"
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


async def fetch_lyrics(q: str | None):
    if not q:
        return None

    params = {"q": q}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{LRCLIB_API_BASE_URL}/search", params=params)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to fetch data from LRCLIB.",
            )
        return response.json()


async def get_spotify_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, data=data)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to get Spotify access token.",
            )
        return response.json()["access_token"]


async def search_spotify_song(track_name: str, artist_name: str, track_limit: int = 1):
    access_token = await get_spotify_access_token()
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    params = {
        "q": f'track:"{track_name}" artist:"{artist_name}"',
        "type": "track",
        "limit": track_limit,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail="Failed to search Spotify for the song.",
            )
        results = response.json()
        tracks = results.get("tracks", {}).get("items", [])
        if not tracks:
            raise HTTPException(status_code=404, detail="Song not found on Spotify.")
        
        return tracks


async def generate_spotify_tracks(track_name: str, artist_name: str, track_limit: int = 1):
    tracks = await search_spotify_song(track_name, artist_name, track_limit)
    return tracks
