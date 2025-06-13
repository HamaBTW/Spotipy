import requests
from bs4 import BeautifulSoup

def check_version(url):
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


print("*"*50)
print(check_version("https://spotipy-app.netlify.app"))
