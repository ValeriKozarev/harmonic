from .matching import to_camelot
import requests

### This module is the wrapper around the APIs that we need for capturing song data

# search the Spotify API for a track, return a simplified list of tracks with only the data we need
def search_tracks(spotify_client, query):
    track_results = spotify_client.search(q=query, type="track")
    tracks_simplified = [
        {
            "track_id": track["id"], 
            "name": track["name"], 
            "artist_id": track["artists"][0]["id"], 
            "artist_name": track["artists"][0]["name"]
        } 
        for track in track_results["tracks"]["items"]]
    
    return tracks_simplified

# this is a helper function to get the reccobeats track ids from the spotify track ids
def _get_reccobeats_track_ids(spotify_track_ids):
    url = "https://api.reccobeats.com/v1/track"
    params = {
        "ids": ",".join(spotify_track_ids)
    }
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    track_dict = {track["href"].split("/")[-1]: track["id"] for track in data["content"]}

    return track_dict

# this is another helper function get the audio features for the given tracks
def _get_audio_features(spotify_track_ids):
    # first we need to convert the track IDs
    track_dict = _get_reccobeats_track_ids(spotify_track_ids)

    audio_feature_data = {}

    # then we need to capture the audio features one by one, since the reccobeats API doesn't support batch requests for audio features
    headers = {
        "Accept": "application/json"
    }

    for spotify_id, reccobeats_id in track_dict.items():
        url = f"https://api.reccobeats.com/v1/track/{reccobeats_id}/audio-features"
        response = requests.get(url, headers=headers)
        audio_feature_data[spotify_id] = response.json()

    return audio_feature_data

# helper function to make it easier to pull together all the data we've gathered
def _merge_track_data(tracks, audio_features):
    # TODO: its possible for a track to be on multiple albums, so we should try to de-dupe by ISRC
    merged_data = []
    for track in tracks:
        track_id = track["track_id"]
        if track_id in audio_features:
            track_to_add = {
                "track_id": track_id,
                "name": track["name"],
                "artist_name": track["artist_name"],
                "camelot_key": to_camelot(audio_features[track_id]["key"], audio_features[track_id]["mode"]),
                "bpm": round(audio_features[track_id]["tempo"]),
                "audio_features": audio_features[track_id],
            }
            merged_data.append(track_to_add)

    return merged_data

# full pipeline of fetching and shaping data for a list of tracks
def get_track_details(tracks):
    spotify_track_ids = [track["track_id"] for track in tracks]
    audio_features = _get_audio_features(spotify_track_ids)

    return _merge_track_data(tracks, audio_features)

# get all of an artist's tracks from Spotify
def get_all_artist_tracks(spotify_client, artist_name):
    # due to how the Spotify APIs are structured, we need to first get the Artist ID, then the list of Album IDs, and then the track IDs for each album
    artist_results = spotify_client.search(q=artist_name, type="artist")
    artist_id = artist_results["artists"]["items"][0]["id"]

    artist_albums_results = spotify_client.artist_albums(artist_id, include_groups="single,album", limit=5) # TODO: add pagination, this only does 5 albums at a time
    album_ids = [album["id"] for album in artist_albums_results["items"]]

    tracks = []
    for album_id in album_ids:
        album_tracks = spotify_client.album_tracks(album_id)
        for track in album_tracks["items"]:
            tracks.append({
                "track_id": track["id"],
                "name": track["name"],
                "artist_id": track["artists"][0]["id"],
                "artist_name": track["artists"][0]["name"]
            })

    return tracks[:40] # TODO: add pagination to this flow (ideally downstream since reccobeats API only takes up to 40 tracks at a time)
