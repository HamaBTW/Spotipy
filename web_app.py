from flask import Flask, request, url_for, session, redirect, render_template
from spotipy.oauth2 import SpotifyOAuth
from pickle import dump, load
from datetime import datetime
import webbrowser
import spotipy
import time

app = Flask(__name__)

app.static_folder = 'static'  # Specify the static folder's name

app.secret_key = "CGFhfgh584DFc2"
app.config["SESSION_COOKIE_NAME"] = "Hama session"
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    oauth_url = sp_oauth.get_authorize_url()
    return redirect(oauth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('selectPlaylist'))

@app.route('/selectPlaylist')
def selectPlaylist():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])

    theme = request.args.get('theme', 'light')  # Default to light theme
    
    # Fetch user profile information
    user_info = sp.current_user()
    display_name = user_info['display_name']
    profile_picture = user_info['images'][0]['url'] if user_info['images'] else None
    
    # Fetch user playlists
    playlists = []
    offset = 0
    while True:
        saved_playlists = sp.current_user_playlists(limit=50, offset=offset)
        playlists.extend(saved_playlists['items'])
        if not saved_playlists['next']:
            break
        offset += 50
    return render_template("playlists.html", playlists=playlists, display_name=display_name, profile_picture=profile_picture, theme=theme)

@app.route('/showSongs/<string:playlist_id>')
def showSongs(playlist_id):
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # Fetch user profile information
    user_info = sp.current_user()
    display_name = user_info['display_name']
    profile_picture = user_info['images'][0]['url'] if user_info['images'] else None

    playlist = sp.playlist(playlist_id)
    tracks = playlist['tracks']['items']

    return render_template("songs.html", playlist_name=playlist['name'], tracks=tracks, playlist_id=playlist_id, display_name=display_name, profile_picture=profile_picture)


@app.route('/exportSongs/<string:playlist_id>')
def exportSongs(playlist_id):
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])

    user_info = sp.current_user()
    display_name = user_info['display_name']

    playlist = sp.playlist(playlist_id)
    tracks = playlist['tracks']['items']
    playlist_name=playlist['name']
    
    # Implement your export logic for the selected playlist here
    # For demonstration purposes, let's just print the track names.

    data = []

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H-%M-%S")

    data_row = {"user_name":display_name, "date":"", "playlist_name":playlist_name, "playlist_tracks":[]}
    for track in tracks:
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        #print(f"{track_name} - {artist_name}")
        data_row["playlist_tracks"].append(f"{track_name} - {artist_name}")

    data_row['date'] = formatted_datetime
    data.append(data_row)


    with open(f"./data/Spotify Data ({formatted_datetime}).shb", "wb+") as f:
        dump(data ,f)
    
    return "Export successful"


@app.route('/exportAllSongs')
def exportAllSongs():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect("/")
    
    sp = spotipy.Spotify(auth=token_info['access_token'])

    user_info = sp.current_user()
    display_name = user_info['display_name']
    
    playlists = []
    offset = 0
    while True:
        saved_playlists = sp.current_user_playlists(limit=50, offset=offset)
        playlists.extend(saved_playlists['items'])
        if not saved_playlists['next']:
            break
        offset += 50
    
    data = []

    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H-%M-%S")

    for playlist in playlists:
        playlist_name = playlist['name']
        playlist_id = playlist['id']
        tracks = sp.playlist_tracks(playlist_id)['items']

        data_row = {"user_name":display_name, "date":"", "playlist_name":playlist_name, "playlist_tracks":[]}
        
        #print(f"Playlist: {playlist_name}")
        for track in tracks:
            track_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            #print(f"    {track_name} - {artist_name}")
            data_row["playlist_tracks"].append(f"{track_name} - {artist_name}")

        data_row['date'] = formatted_datetime
        data.append(data_row)



    with open(f"./data/Spotify Data ({formatted_datetime}).shb", "wb+") as f:
        dump(data ,f)
    
    return "Export successful"


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="870fbcd0954446088a4de2553863b40e",
        client_secret="5e706285917245d4a45c77fd11f58eca",
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read user-read-private user-read-email"
    )

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception("Token not found")
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

if __name__ == "__main__":
    url = "http://localhost:5000"
    webbrowser.open(url)
    app.run(debug=True)

