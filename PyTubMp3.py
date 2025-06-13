import requests
import os

class YtbToMp3():
    """Download a given YouTube link in MP3 by the video ID"""

    def __init__(self, video_id, titels, folder_path, key):
        """
        Initialize the YtbToMp3 class.

        :param video_id (str): Video ID as a string
        :param titels (list of str): titels of all downloaded songs
        """
        if not isinstance(video_id, str):
            raise ValueError("Video ID must be a string")
        
        self.video_id = video_id
        self.titels = titels
        self.folder_path = folder_path
        self.key = key

    def Download(self):
        url = "https://youtube-mp36.p.rapidapi.com/dl"

        querystring = {"id": self.video_id}

        headers = {
            "X-RapidAPI-Key": self.key, #"7f55ded0a1mshd7a6f932ac25b45p17b043jsnca602366efde",
            "X-RapidAPI-Host": "youtube-mp36.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        data = response.json()
        print(data)

        if "link" in data:
            audio_download_link = data["link"]
            print("Download link:", audio_download_link)
        else:
            print("Audio download link not found in response.")
        

        try:
            response2 = requests.get(audio_download_link)
        except:
            pass

        print("data :",data)


        if 'message' in data and "You have exceeded the DAILY quota for Request on your current plan" in data['message']:
            print("You have exceeded the DAILY quota for Request on your current plan")
            return "free plan"

        if response2.status_code == 200:
            # Sanitize the title to create a valid file name
            sanitized_title = "".join(c if c.isalnum() or c in "._-" else "_" for c in data['title'])
            file_path = os.path.join(self.folder_path, f"{sanitized_title}.mp3")

            if not f"{sanitized_title}.mp3" in (self.titels):
                # print(self.titels)
                # print(sanitized_title)
                # print(file_path)

                with open(file_path, "wb") as audio_file:
                    audio_file.write(response2.content)

                print("Audio file downloaded successfully.")
            else:
                print("Audio file already downloaded.")
            return "done"
        else:
            print("Failed to download audio. Status code:", response2.status_code)
            return "error"