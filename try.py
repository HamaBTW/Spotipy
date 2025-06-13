from PyTubSearch import YtbSearch
from PyTubMp3 import YtbToMp3

keyword = "Ticking Away ft. Grabbitz & bbno$ (clip officiel)"
file_path = "./data"

data = YtbSearch.Search(keyword)

video_id = data["video_id"]
ytb_to_mp3 = YtbToMp3(video_id, file_path)
ytb_to_mp3.Download()

