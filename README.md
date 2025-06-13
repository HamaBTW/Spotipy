# Spotipy - Spotify Playlist Manager & Music Downloader

<div align="center">
  <img src="img.png" alt="Spotipy Application Screenshot"/>
  <br/>
  <em>Spotipy Desktop Application Interface</em>
</div>

<br/>

A comprehensive Spotify application suite that allows users to manage their Spotify playlists and download music from YouTube. The project includes both web and desktop interfaces with modern UI design and powerful features.

## 🚀 Features

### Core Functionality
- **Spotify Integration**: Full OAuth authentication with Spotify API
- **Playlist Management**: View, browse, and export Spotify playlists
- **Music Download**: Download songs from YouTube based on Spotify playlist data
- **Multi-Interface**: Both web-based and desktop GUI applications
- **Theme Support**: Dark and light theme options
- **Progress Tracking**: Real-time download progress with visual indicators

### Web Application Features
- Clean, responsive web interface
- User profile display with profile pictures
- Playlist browsing and song viewing
- Export functionality for individual playlists or all songs
- Theme toggle with persistent settings
- Modern CSS styling with smooth transitions

### Desktop Application Features
- Native desktop GUI built with Flet framework
- Advanced download management with progress bars
- API key configuration for YouTube downloads
- Batch download capabilities
- Custom window controls and modern UI
- Automatic update checking

## 🛠️ Technologies

### Backend & Core
- **Python 3.7+** - Main programming language
- **Flask** - Web framework for the web application
- **Spotipy** - Spotify Web API Python library
- **OAuth 2.0** - Secure authentication with Spotify

### Frontend & UI
- **Flet** - Modern Python framework for desktop GUI applications
- **HTML5/CSS3** - Web interface markup and styling
- **JavaScript** - Client-side functionality and theme switching
- **Font Awesome** - Icon library for modern UI elements

### APIs & Services
- **Spotify Web API** - Access to user playlists and music data
- **YouTube Data API v3** - Video search functionality
- **RapidAPI YouTube MP3** - Audio conversion and download service
- **Google API Client** - YouTube API integration

### Data & Storage
- **Pickle** - Python object serialization for data persistence
- **JSON** - Configuration and API response handling
- **Local File System** - Music downloads and application data

### Development & Build Tools
- **PyInstaller** - Creating standalone executable applications
- **youtube-search-python** - YouTube search without API quotas
- **BeautifulSoup4** - Web scraping for update checking
- **Requests** - HTTP library for API calls

### UI Libraries & Frameworks
- **Material Design** - Design principles for desktop application
- **CSS Grid/Flexbox** - Modern web layout techniques
- **LocalStorage API** - Persistent theme preferences in web app

## 🏗️ Project Structure

```
spotipy/
├── web_app6.py              # Main web application (latest version)
├── gui_app12.py             # Main desktop application (latest version)
├── PyTubSearch.py           # YouTube search functionality
├── PyTubMp3.py             # YouTube to MP3 download functionality
├── templates/               # HTML templates for web interface
│   ├── playlists.html      # Playlist listing page
│   └── songs.html          # Song listing page
├── static/                  # Static web assets
│   ├── styles.css          # Main stylesheet
│   ├── theme.js            # Theme switching functionality
│   └── icon.ico            # Application icon
├── assets/                  # Application assets
│   ├── app-screenshot.png  # Main application screenshot
│   ├── favicon.png         # Application favicon
│   └── icon.ico            # Application icon
├── data/                    # Application data storage
├── output/                  # Downloaded music output directory
├── build/                   # PyInstaller build files
└── *.spec                  # PyInstaller specification files
```

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- Spotify Developer Account (for API credentials)
- RapidAPI Account (for YouTube download functionality)

### Required Dependencies
```bash
pip install flask
pip install spotipy
pip install flet
pip install requests
pip install youtube-search-python
pip install google-api-python-client
pip install beautifulsoup4
pip install pyinstaller  # For creating executables
```

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd spotipy
   ```

2. **Spotify API Setup**
   - Create a Spotify app at [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Note your Client ID and Client Secret
   - Set redirect URI to `http://localhost:5000/redirect`

3. **Configure API Credentials**
   - Create `data/web app data.wbspy` file with your Spotify credentials
   - Or modify the hardcoded credentials in the application files

4. **YouTube API Setup** (Optional)
   - Get a YouTube Data API key from Google Cloud Console
   - Get a RapidAPI key for YouTube MP3 conversion
   - Configure in the application settings

5. **Add Application Screenshots** (Optional)
   - Create an `assets/` directory in the project root
   - Add your application screenshots as `app-screenshot.png`
   - Update the README image path if using a different filename

## 🚀 Usage

### Web Application
```bash
python web_app6.py
```
- Automatically opens browser to `http://localhost:5000`
- Login with your Spotify account
- Browse and export your playlists

### Desktop Application
```bash
python gui_app12.py
```
- Modern desktop interface with native controls
- Advanced download features and progress tracking
- API key management interface

## 🔧 Configuration

### Spotify Credentials
The application expects Spotify credentials in `data/web app data.wbspy`:
```python
{
    "client_id": "your_spotify_client_id",
    "client_secret": "your_spotify_client_secret"
}
```

### API Keys
YouTube download functionality requires API keys stored in `data/spotipy data api key.spky`:
```python
{
    "key": "your_rapidapi_key",
    "type": "Custom"  # or "Default"
}
```

## 📱 Application Versions

### Web Applications
- `web_app6.py` - Latest stable web version
- `web_app5.py` - Previous version with data management
- `PySpotyWeb.py` - Original web implementation

### Desktop Applications
- `gui_app12.py` - Latest with update checking
- `gui_app11.py` - Enhanced UI version
- `gui_app10.py` - Stable desktop version
- Earlier versions (`gui_app*.py`) - Development iterations

## 🎵 Download Functionality

The application can download music from YouTube by:
1. Searching YouTube for songs based on Spotify track information
2. Using RapidAPI's YouTube MP3 conversion service
3. Organizing downloads by playlist and date
4. Avoiding duplicate downloads

### Supported Features
- Batch downloading of entire playlists
- Individual song downloads
- Progress tracking with visual indicators
- Automatic folder organization
- Duplicate detection and prevention

## 🔨 Building Executables

The project includes PyInstaller specifications for creating standalone executables:

```bash
# Web application executable
pyinstaller "Spotipy web connector.spec"

# Desktop application executable
pyinstaller "Spotipy.spec"
```

## 🎨 Themes and UI

### Web Interface
- Responsive design with CSS Grid/Flexbox
- Dark/Light theme toggle with localStorage persistence
- Font Awesome icons for modern UI elements
- Smooth transitions and hover effects

### Desktop Interface
- Native window controls (minimize, maximize, close)
- Custom app bar with drag functionality
- Material Design inspired components
- Progress bars and status indicators

## 📊 Data Management

The application manages various types of data:
- **Spotify Data**: Playlists, tracks, user information
- **Configuration**: API keys, user preferences
- **Downloads**: Organized by playlist and date
- **Cache**: Temporary authentication tokens

## 🔐 Security Notes

- Spotify credentials are stored locally in binary format
- API keys are managed securely within the application
- OAuth tokens are handled according to Spotify's guidelines
- No sensitive data is transmitted to external services (except APIs)

## 🤝 Contributing

This project shows multiple development iterations and approaches. When contributing:
1. Focus on the latest versions (`web_app6.py`, `gui_app12.py`)
2. Maintain backward compatibility where possible
3. Follow the existing code structure and naming conventions
4. Test both web and desktop interfaces

## 📄 License

[Add your license information here]

## 🙏 Acknowledgments

- Spotify Web API for music data
- YouTube and RapidAPI for download functionality
- Flet framework for desktop GUI
- Flask framework for web interface
