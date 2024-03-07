import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()
# 从.env文件中读取API Key
x_api_key = os.getenv("X_API_KEY")
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": x_api_key
}


def get_caption_video_id(video_id):
    url = "https://api.heygen.com/v1/video/caption.generate"
    payload = {"video_id": video_id}
    response = requests.post(url, json=payload, headers=headers)
    add_caption_video_id = response.json()["data"]["video_id"]

    return add_caption_video_id


def download_caption_video(add_caption_video_id):
    get_url = f"https://api.heygen.com/v1/video/caption.get?video_id={add_caption_video_id}"

    while True:
        response = requests.get(get_url, headers=headers)
        data = response.json()["data"]
        caption_status = data['caption_status']

        if caption_status == 2:
            caption_video_url = data['caption_video_url']
            # 下载视频并保存
            caption_video_response = requests.get(
                caption_video_url, headers=headers)
            outputFile = f"./output/{add_caption_video_id}_caption_output.mp4"
            with open(outputFile, "wb") as f:
                f.write(caption_video_response.content)
            print(f"带字幕的视频已保存到{outputFile}")
            break
        elif caption_status == 3:
            error = data['error']
            print(error["code"], error["detail"])
            break
        else:
            time.sleep(20)
            print(data)


if __name__ == "__main__":
    video_id = "16ddb45a27a745928e2ee7e8576ca6b1"
    # add_caption_video_id = get_caption_video_id(video_id)
    download_caption_video(video_id)
