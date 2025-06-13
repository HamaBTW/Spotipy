from youtubesearchpython import VideosSearch
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests


# Replace 'YOUR_API_KEY' with the actual API key you obtained from the Google Cloud Console
API_KEY = 'AIzaSyBUrkghjVo1dV6qmt5qx1n0DPcVJNQ3wBM'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

class YtbSearch():
    """Search for a given keyword on YouTube"""

    def __init__(self, query):
        """
        Initialize the YtbSearch class.

        :param keyword (str): Keyword as a string
        """
        if not isinstance(query, str):
            raise ValueError("Keyword must be a string")
        
        self.query = query

    def Search(keyword):
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    
        search_response = youtube.search().list(
            q=keyword,
            type='video',
            part='id,snippet',
            maxResults=10
        ).execute()
        
        videos = []
        for search_result in search_response.get('items', []):
            video = {
                'title': search_result['snippet']['title'],
                'video_id': search_result['id']['videoId'],
                'thumbnail': search_result['snippet']['thumbnails']['default']['url']
            }
            videos.append(video)
        
        v_id = videos[0]['video_id']
        link = "https://www.youtube.com/watch?v=" + v_id

        return {"video_link":link, "video_id":v_id}

    def Search2(keyword):
        num_results = 1
        videos_search = VideosSearch(keyword, limit=num_results)
        results = []

        for result in videos_search.result()['result']:
            video_id = result['id']
            video_title = result['title']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            results.append({
                'video_id': video_id,
                'video_title': video_title,
                'video_url': video_url
            })
        
        v_id = results[0]['video_id']
        link = results[0]['video_url']

        return {"video_link":link, "video_id":v_id}

class AppUpdate():    
    def check_version(self, url):
        version = "unkown"
        try:

            # Fetch the HTML content of the webpage
            response = requests.get(url)

            if response.status_code == 200:
                html_content = response.content
                soup = BeautifulSoup(html_content, 'html.parser')

                # Example: Extract all text within <p> tags
                paragraphs = soup.find_all('p')

                for paragraph in paragraphs:
                    if "Current Version: " in paragraph.get_text():
                        version = paragraph.get_text().split('Current Version: ')[1].replace(' ', '')
        except:
            pass

        return version
    
    
