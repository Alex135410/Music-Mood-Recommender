import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import logging

app = Flask(__name__)
CORS(app)

# Spotify credentials (you will put your credentials here)
CLIENT_ID = 'YOUR_SPOTIFY_CREDENTIALS'
CLIENT_SECRET = 'YOUR_SPOTIFY_CREDENTIALS'

def get_spotify_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        'Authorization': f'Basic {auth_header}',
    }
    data = {'grant_type': 'client_credentials'}
    response = requests.post(auth_url, headers=headers, data=data)
    response.raise_for_status()
    token = response.json()['access_token']
    return token

def search_playlists(mood, token):
    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'q': mood,
        'type': 'playlist',
        'limit': 1
    }
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_playlist_tracks(playlist_id, token):
    tracks_url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(tracks_url, headers=headers)
    response.raise_for_status()
    return response.json()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "text" not in data or not data["text"].strip():
        return jsonify({"error": "No text provided"}), 400

    text = data["text"].strip()
    app.logger.info(f"Received text: {text}")

    # TODO: Replace this with your actual mood prediction model
    predicted_mood = text.lower()

    try:
        token = get_spotify_token()
        search_results = search_playlists(predicted_mood, token)
        playlists = search_results.get('playlists', {}).get('items', [])

        if not playlists:
            return jsonify({"error": f"No playlists found for mood '{predicted_mood}'"}), 404

        playlist = playlists[0]
        playlist_id = playlist['id']

        tracks_data = get_playlist_tracks(playlist_id, token)
        tracks = tracks_data.get('items', [])

        # Extract track info: name and artists
        songs = []
        for item in tracks:
            track = item.get('track')
            if track:
                name = track.get('name', 'Unknown Song')
                artists = ', '.join(artist.get('name', 'Unknown Artist') for artist in track.get('artists', []))
                songs.append({"name": name, "artists": artists})

        return jsonify({
            "mood": predicted_mood,
            "playlist_name": playlist.get('name', 'Unknown Playlist'),
            "songs": songs
        })

    except requests.HTTPError as e:
        app.logger.error(f"HTTP error during Spotify API call: {e}")
        return jsonify({"error": "Failed to fetch data from Spotify API"}), 500
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
