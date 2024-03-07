import requests
import os
from dotenv import load_dotenv
from download_video import download_video
from add_caption import get_caption_video_id, download_caption_video


load_dotenv()
# 从.env文件中读取API Key
x_api_key = os.getenv("X_API_KEY")

generate_url = "https://api.heygen.com/v1/video.generate"

payload = {
    "background": "#ffffff",
    "ratio": "16:9",
    "test": True,
    "caption_open": False,
    "version": "v1alpha",
    "clips": [
        {
            "avatar_id": "Daisy-inskirt-20220818",
            "avatar_style": "normal",
            "input_text": "欢迎来到河马世界，我是一只大河马，是不是让你很吃惊呢？",
            "offset": {
                "x": 0,
                "y": 0
            },
            "scale": 1,
            "voice_id": "25ef3e4d1a4846a58a5f4c3b1a7f70a8"
        }
    ],
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": x_api_key
}

# 生成视频，获得视频id
response = requests.post(generate_url, json=payload, headers=headers)
video_id = response.json()["data"]["video_id"]

print("video_id:", video_id)

# 下载并保存视频:无字幕
download_video(video_id)

# 如果想要下载并保存有字幕的视频，可以使用下面的语句
# add_caption_video_id = get_caption_video_id(video_id)
# download_caption_video(add_caption_video_id)
