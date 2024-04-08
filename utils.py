import re
import os
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

#Setting global parameters:
error_429_occurred = False

def extract_playlist_id(link):
    # Regular expression to extract the playlist ID
    regex = r"/playlist/(\w+)\?"
    match = re.search(regex, link)
    if match:
        playlist_id = match.group(1)
        return playlist_id
    else:
        return None

def load_playlist(playlist_id):
    # Spotify API credentials
    global client_id
    global client_secret
    if 'client_id' not in globals() or 'client_secret' not in globals():
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Authenticate with Spotify API
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    global sp
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    filename = f'{playlist_id}.json'

    # Fetch the playlist data
    playlist_name = sp.playlist(playlist_id)['name']

    # Update playlists.json with playlist ID and name
    update_playlists_json({'id': playlist_id, 'name': playlist_name})

    # Fetch and save playlist data
    save_playlist_data(playlist_id, filename)

    # Load the saved playlist data
    playlist_data = load_playlist_data(filename)
        
    return playlist_data

# def update_playlists_json(new_playlist_info):
#     playlists_file = "resources/playlists.json"
#     if not os.path.exists(playlists_file):
#         with open(playlists_file, 'w') as f:
#             json.dump([], f)

#     # Load existing playlist info
#     with open(playlists_file, 'r') as f:
#         existing_playlists = json.load(f)

#     # Check if playlist ID already exists
#     playlist_ids = [playlist['id'] for playlist in existing_playlists]
#     if new_playlist_info['id'] not in playlist_ids:
#         existing_playlists.append(new_playlist_info)
#         # Update playlists.json with new playlist info
#         with open(playlists_file, 'w') as f:
#             json.dump(existing_playlists, f, indent=4)  # Use indentation for better readability

#     return

def update_playlists_json(new_playlist_info):
    playlists_file = "resources/playlists.json"
    if not os.path.exists(playlists_file):
        with open(playlists_file, 'w') as f:
            json.dump([], f)

    # Load existing playlist info
    with open(playlists_file, 'r') as f:
        try:
            existing_playlists = json.load(f)
        except json.decoder.JSONDecodeError:
            existing_playlists = []

    # Check if playlist ID already exists
    playlist_ids = [playlist['id'] for playlist in existing_playlists]
    if new_playlist_info['id'] not in playlist_ids:
        existing_playlists.append(new_playlist_info)
        # Update playlists.json with new playlist info
        with open(playlists_file, 'w') as f:
            json.dump(existing_playlists, f, indent=4)  # Use indentation for better readability

    return


def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def fetch_track_info(track):
    track_info = {
        'name': track['track']['name'],
        'artists': [artist['name'] for artist in track['track']['artists']],
        'album': track['track']['album']['name'],
        'release_date': track['track']['album']['release_date'],
        'duration_ms': track['track']['duration_ms'],
        'popularity': track['track']['popularity'],
        'id': track['track']['id']  # Include track ID
    }

    # Call the fetch_track_audio_features function to get audio features
    audio_features = fetch_track_audio_features(track['track']['id'])
    if audio_features:
        # Add audio features to track_info
        track_info.update(audio_features)
    return track_info

# def save_playlist_data(playlist_id, filename):
#     tracks = get_playlist_tracks(playlist_id)
#     playlist_data = []
#     for track in tracks:
#         playlist_data.append(fetch_track_info(track))
#     # Prepend the filename with the path to the resources directory
#     filepath = os.path.join("resources/playlists", filename)
#     with open(filepath, 'w') as f:
#         json.dump(playlist_data, f)

def save_playlist_data(playlist_id, filename):
    # Fetch the playlist details including its name
    playlist_info = sp.playlist(playlist_id)

    # Get the playlist name
    playlist_name = playlist_info['name']

    # Fetch and save playlist data
    tracks = get_playlist_tracks(playlist_id)
    playlist_data = []
    for track in tracks:
        playlist_data.append(fetch_track_info(track))
    # Prepend the filename with the path to the resources directory
    filepath = os.path.join("resources/playlists", filename)
    with open(filepath, 'w') as f:
        json.dump(playlist_data, f, indent = 4)

def load_playlist_data(filename):
    # Prepend the filename with the path to the resources directory
    filepath = os.path.join("resources/playlists", filename)

    # Check if the file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filename}' not found in resources directory.")

    with open(filepath, 'r') as f:
        playlist_data = json.load(f)
    return playlist_data

def fetch_track_audio_features(track):
    # Don't run if 429 occured
    global error_429_occurred
    if error_429_occurred:
        return None
    
    try:
        # Make an API request to fetch audio features for the track
        audio_features = sp.audio_features(track)
        
        if audio_features:
            # Extract relevant audio features
            track_audio_features = {
                'danceability': audio_features[0]['danceability'],
                'energy': audio_features[0]['energy'],
                'key': audio_features[0]['key'],
                'loudness': audio_features[0]['loudness'],
                'mode': audio_features[0]['mode'],
                'speechiness': audio_features[0]['speechiness'],
                'acousticness': audio_features[0]['acousticness'],
                'instrumentalness': audio_features[0]['instrumentalness'],
                'liveness': audio_features[0]['liveness'],
                'valence': audio_features[0]['valence'],
                'tempo': audio_features[0]['tempo'],
            }
            return track_audio_features
        else:
            return None
    except spotipy.SpotifyException as e:
        # Handle 429 error
        error_429_occurred = True
        print(f"Error fetching audio features for track {track}: {e}")
        return None