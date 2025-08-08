# Music Mood Recommender

A web application that predicts the user's mood from text input and recommends Spotify playlists and songs matching that mood.

---

## Table of Contents

- [Architecture](#architecture)  
- [Environment](#environment)  
- [Executing the Web Application](#executing-the-web-application)  

---

## Architecture

This project follows a client-server architecture:

- **Frontend (Client):**  
  - A single-page web application built with HTML, CSS, and JavaScript.  
  - Provides a clean UI where users input their mood or feelings.  
  - Sends requests to the backend server and displays recommended playlists and songs.  

- **Backend (Server):**  
  - Built using Python with Flask as the web framework.  
  - Receives user input from the frontend via API endpoints.  
  - Uses the Spotify API to search and retrieve playlist and song recommendations based on the mood text.  
  - Handles error cases such as empty input or no results found.

- **Third-Party API:**  
  - Spotify Web API is used to search for playlists and fetch track details.

---

## Environment

To run this project, your device must have:

- **Python 3.7+** installed  
- **pip** (Python package installer)  
- A Spotify Developer account and registered app to get:  
  - `SPOTIFY_CLIENT_ID`  
  - `SPOTIFY_CLIENT_SECRET`

- Recommended to use a virtual environment (e.g., `venv`) to isolate dependencies.

---

## Executing the Web Application

Follow these steps to deploy and run the Music Mood Recommender locally:

1. **Clone the repository** (if applicable)  
   ```bash
   git clone https://github.com/yourusername/music-mood-recommender.git
   cd music-mood-recommender/server
2. **Create and activate a virtual environment** (optional but recommended)
   ```bash
   python3 -m venv venv
   source venv/bin/activate     # On Windows use: venv\Scripts\activate
3. **Install required Python packages**
   ```bash
   pip install -r requirements.txt
4. **Set environment variables for Spotify credentials**
   On macOS/Linux:
   ```bash
   export SPOTIFY_CLIENT_ID='your_client_id_here'
   export SPOTIFY_CLIENT_SECRET='your_client_secret_here'
   On Windows (PowerShell):
   ```powershell
   setx SPOTIFY_CLIENT_ID "your_client_id_here"
   setx SPOTIFY_CLIENT_SECRET "your_client_secret_here"
5. **Run the Flask server**
   `bash
   python app.py
6. **Open the frontend**
   Open the index.html file in your preferred browser (either directly or through a local server)
7. **Use the application**
   - Enter a mood or feeling in the input box.
   - Submit to receive a recommended playlist and song list from Spotify.

   

   

   


  

