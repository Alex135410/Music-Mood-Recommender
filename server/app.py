from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)
CORS(app)

# Load your model pipeline (vectorizer + classifier)
model = joblib.load("../model/mood_classifier.pkl")

# === Spotify API credentials ===
SPOTIFY_CLIENT_ID = '32cdd36cd9a948bfae976cd9f67746e4'
SPOTIFY_CLIENT_SECRET = '66a9e1ebf0904b3083b38ee161d80aee'

spotify_auth_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)

sp = spotipy.Spotify(auth_manager=spotify_auth_manager)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Predict mood using your trained model pipeline
        prediction = model.predict([text])[0]

        songs = []
        results = sp.search(q=prediction, type='playlist', limit=1)
        app.logger.info(f"Spotify search results: {results}")

        playlists = results.get('playlists') or {}
        items = playlists.get('items') or []

        # Find first valid playlist item (skip None)
        playlist = next((item for item in items if item is not None), None)

        if playlist is None:
            app.logger.warning(f"No valid playlists found for mood: {prediction}")
            return jsonify({
                "mood": prediction,
                "songs": [],
                "warning": "No valid playlists found for this mood."
            })

        playlist_id = playlist['id']
        tracks = sp.playlist_tracks(playlist_id, limit=5)
        for item in tracks['items']:
            track = item['track']
            songs.append({
                'title': track['name'],
                'artist': track['artists'][0]['name'],
                'url': track['external_urls']['spotify']
            })

        return jsonify({
            "mood": prediction,
            "songs": songs
        })

    except Exception as e:
        app.logger.error(f"Error in /predict: {e}", exc_info=True)
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
