from flask import Flask, request, redirect, session, render_template
import requests
import base64
import json

app = Flask(__name__)
app.secret_key = "Hama"
SPOTIFY_CLIENT_ID = "870fbcd0954446088a4de2553863b40e"
SPOTIFY_CLIENT_SECRET = "5e706285917245d4a45c77fd11f58eca"
SPOTIFY_REDIRECT_URI = "http://localhost:5000/callback"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    scopes = "user-library-read playlist-read-private"
    auth_url = f"https://accounts.spotify.com/authorize?client_id={SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={SPOTIFY_REDIRECT_URI}&scope={scopes}"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    auth_code = request.args.get("code")
    # Exchange authorization code for access token and refresh token
    # Handle the API request and token handling here

@app.route("/playlists")
def playlists():
    access_token = session.get("access_token")
    # Make API request to fetch user's playlists using the access token
    # Handle the API request and playlist processing here
    # Render the playlist data in an HTML template

if __name__ == "__main__":
    app.run(debug=True)
