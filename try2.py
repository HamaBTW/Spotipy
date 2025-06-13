import urllib.parse
import urllib.request
import re

class YtbSearch():
    """Search for a given keyword on YouTube"""

    def __init__(self, keyword):
        """
        Initialize the YtbSearch class.

        :param keyword (str): Keyword as a string
        """
        if not isinstance(keyword, str):
            raise ValueError("Keyword must be a string")
        
        self.keyword = keyword

    def Search(keyword):

        search_keyword = urllib.parse.quote(keyword)  # URL-encode the keyword
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

        link = "https://www.youtube.com/watch?v=" + video_ids[0]

        return link

keyword = "Ticking Away ft. Grabbitz & bbno$ (clip officiel)"

print(YtbSearch.Search(keyword))