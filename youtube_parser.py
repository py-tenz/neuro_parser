import requests
import json
from config import YT_API_KEY

UNI_URL = "https://www.googleapis.com/youtube/v3/search"
COMMENTS_URL = "https://www.googleapis.com/youtube/v3/commentThreads"
HASHTAG = "#programming"

def post_vids(h1, h2):
    params = {
        "part": "snippet",
        "q": h1 + " #shorts" + h2,
        "type": "video",
        "videoDuration": "short",
        "maxResults": 50,
        "key": YT_API_KEY
    }
    response = requests.get(UNI_URL, params=params)
    with open('data/yt_videos.json', 'w', encoding='utf-8') as f:
        f.write(response.text)

def get_all_video_ids():
    with open("data/yt_videos.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        video_ids = []
        for item in data.get("items", []):
            video_ids.append(item["id"]["videoId"])
        return video_ids
    
def get_all_yt_video_comments(video_ids: list):
    for i in video_ids:
        comments_params = {
            "part": "snippet",
            "videoId": i,
            "maxResults": 100,
            "textFormat": "plainText",
            "key": YT_API_KEY
        }
        response = requests.get(COMMENTS_URL, params=comments_params)
        with open(f'data/yt_comments.json', 'w', encoding='utf-8') as f:
            f.write(response.text)

def get_comments_as_list():
    with open("data/yt_comments.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        all_comments = []
        for i in data.get("items", []):
            all_comments.append(i['snippet']['topLevelComment']["snippet"]["textDisplay"])
        return all_comments

# get_all_yt_video_comments(get_all_video_ids())


        
        