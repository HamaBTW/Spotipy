from flask import Flask, request, url_for, session, redirect, render_template
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import webbrowser
import time
from datetime import datetime
from pickle import dump, load

class SpotifyApp:
    def __init__(self, client_id, client_secret, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        
        self.app = Flask(__name__, static_folder="static", template_folder="templates")

        self.app.secret_key = "CGFhfgh584DFc2"
        self.app.config["SESSION_COOKIE_NAME"] = "Hama session"
        self.TOKEN_INFO = "token_info"
        
        self.redirect_path = 'handle_redirect'  # Update the route name
        
        self.create_routes()

    def create_routes(self):
        self.app.route('/')(self.login)
        self.app.route('/redirect')(self.handle_redirect)
        self.app.route('/selectPlaylist')(self.selectPlaylist)
        self.app.route('/showSongs/<string:playlist_id>')(self.showSongs)
        self.app.route('/exportSongs/<string:playlist_id>')(self.exportSongs)
        self.app.route('/exportAllSongs')(self.exportAllSongs)
    
    def run(self):
        url = "http://localhost:5000"
        webbrowser.open(url)
        self.app.run(debug=False)
    
    def create_spotify_oauth(self):
        redirect_uri = url_for(self.redirect_path, _external=True)  # Use url_for here
        return SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=redirect_uri,
            scope=self.scope
        )
    
    def get_token(self):
        token_info = session.get(self.TOKEN_INFO, None)
        if not token_info:
            raise Exception("Token not found")
        now = int(time.time())
        is_expired = token_info['expires_at'] - now < 60
        if is_expired:
            sp_oauth = self.create_spotify_oauth()
            token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        return token_info
    
    def login(self):
        sp_oauth = self.create_spotify_oauth()
        oauth_url = sp_oauth.get_authorize_url()
        return redirect(oauth_url)
    
    def handle_redirect(self):
        sp_oauth = self.create_spotify_oauth()
        session.clear()
        code = request.args.get('code')
        token_info = sp_oauth.get_access_token(code)
        session[self.TOKEN_INFO] = token_info
        return redirect(url_for('selectPlaylist'))
         
    def selectPlaylist(self):
        try:
            token_info = self.get_token()
        except:
            print("User not logged in")
            return redirect("/")
        
        sp = spotipy.Spotify(auth=token_info['access_token'])
        sp.trace = False  # Turn off tracing to avoid printing too much debug information
        
        theme = request.args.get('theme', 'light')
        
        user_info = sp.current_user()
        display_name = user_info['display_name']
        profile_picture = user_info['images'][0]['url'] if user_info['images'] else None
        
        playlists = []
        offset = 0
        while True:
            saved_playlists = sp.current_user_playlists(limit=50, offset=offset)
            playlists.extend(saved_playlists['items'])
            if not saved_playlists['next']:
                break
            offset += 50
        print(len(playlists))
        return render_template("playlists.html", playlists=playlists, display_name=display_name, profile_picture=profile_picture, theme=theme)    
    
    def showSongs(self, playlist_id):
        try:
            token_info = self.get_token()
        except:
            print("User not logged in")
            return redirect("/")
        
        sp = spotipy.Spotify(auth=token_info['access_token'])
    
        user_info = sp.current_user()
        display_name = user_info['display_name']
        profile_picture = user_info['images'][0]['url'] if user_info['images'] else None
    
        playlist = sp.playlist(playlist_id)

        # Fetch all tracks using pagination
        tracks = []
        offset = 0
        while True:
            playlist_tracks = sp.playlist_tracks(playlist_id, offset=offset)
            tracks.extend(playlist_tracks['items'])
            if not playlist_tracks['next']:
                break
            offset += len(playlist_tracks['items'])
    
        return render_template("songs.html", playlist_name=playlist['name'], tracks=tracks, playlist_id=playlist_id, display_name=display_name, profile_picture=profile_picture)
    
    def exportSongs(self, playlist_id):
        try:
            token_info = self.get_token()
        except:
            print("User not logged in")
            return redirect("/")
        
        sp = spotipy.Spotify(auth=token_info['access_token'])
    
        user_info = sp.current_user()
        display_name = user_info['display_name']
    
        playlist = sp.playlist(playlist_id)

        # Fetch all tracks using pagination
        tracks = []
        offset = 0
        while True:
            playlist_tracks = sp.playlist_tracks(playlist_id, offset=offset)
            tracks.extend(playlist_tracks['items'])
            #for _ in tracks:
                # f=open("gg.txt", "a", encoding="utf-8")
                # print(_['track']['name'])
                # f.write(_['track']['name']+"\n")
                # f.close()
            if not playlist_tracks['next']:
                break
            offset += len(playlist_tracks['items'])

        playlist_name = playlist['name']
    
        data = []
    
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H-%M-%S")
    
        data_row = {"user_name": display_name, "date": "", "playlist_name": playlist_name, "playlist_tracks": [], "error_tracks": []}
        for track in tracks:
            track_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            data_row["playlist_tracks"].append(f"{track_name} - {artist_name}")
    
        data_row['date'] = formatted_datetime
        data.append(data_row)
    
        f_name = f"./data/Spotify Data ({formatted_datetime}).shb"
        # Replace invalid characters
        f_name = f_name.replace("<", "").replace(">", "")
        # Replace spaces and other invalid characters
        f_name = f_name.replace(" ", "_").replace(":", "-")
        with open(f_name, "wb+") as f:
            dump(data, f)
        
        return "Export successful"
    
    def exportAllSongs(self):
        try:
            token_info = self.get_token()
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
    
        for playlist in playlists:
            data = []
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d %H-%M-%S-%f")

            playlist_name = playlist['name']
            playlist_id = playlist['id']
            
            # Fetch all tracks using pagination
            tracks = []
            offset = 0
            while True:
                playlist_tracks = sp.playlist_tracks(playlist_id, limit=100, offset=offset)
                tracks.extend(playlist_tracks['items'])
                if not playlist_tracks['next']:
                    break
                offset += 100
            
    
            data_row = {"user_name": display_name, "date": "", "playlist_name": playlist_name, "playlist_tracks": [], "error_tracks": []}
            #print(data_row['playlist_name'])
            for track in tracks:
                track_name = track['track']['name']
                artist_name = track['track']['artists'][0]['name']
                data_row["playlist_tracks"].append(f"{track_name} - {artist_name}")
    
            data_row['date'] = formatted_datetime

            f_name = f"./data/Spotify Data ({formatted_datetime}).shb"
            # Replace invalid characters
            f_name = f_name.replace("<", "").replace(">", "")
            # Replace spaces and other invalid characters
            f_name = f_name.replace(" ", "_").replace(":", "-")

            data.append(data_row)

        
            with open(f_name, "wb+") as f:
                dump(data, f)
        
        return "Export successful"

if __name__ == "__main__":

    app = SpotifyApp(
        client_id= 'Your Client ID',
        client_secret= 'Your Client Secret',
        scope="user-library-read user-read-private user-read-email playlist-read-private playlist-read-collaborative"
    )

    app.run()
    

