import requests
import os
from dotenv import load_dotenv
from typing import List, Dict, Any, Union
import time

load_dotenv()
# 从.env文件中读取API Key
stablity_api_key = os.getenv("STABILITY_API_KEY")
print(stablity_api_key)

# 特别要注意，image只支持三种大小，分别是1024x576 576x1024 768x768

# curl -f -sS "https://api.stability.ai/v2alpha/generation/image-to-video" -H "authorization: Bearer sk-XpP3t1urDRKvZmmLtRhNvsCDLoCkGfFRk5ihXWn6maLPuqzg" -F image=@"../test/test.png" -F seed=0 -F cfg_scale=1.8 -F motion_bucket_id=127 -o "./output.json"


def image_to_video(image: str) -> str:
    response = requests.post(
        f"https://api.stability.ai/v2alpha/generation/image-to-video",
        headers={
            "Authorization": f"Bearer {stablity_api_key}",
        },
        files={"image": open(image, "rb")},
        data={
            "seed": 0,
            "cfg_scale": 1.8,
            "motion_bucket_id": 127
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    if response.json.get('id'):
        return response.json().get('id')
    else:
        errors = response.json.get('errors')[0]
        print(errors)
        return ""


def get_video(generation_id: str):
    if generation_id == "":
        return

    response = requests.request(
        "GET",
        f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{generation_id}",
        headers={
            'Accept': "video/*",  # Use 'application/json' to receive base64 encoded JSON
            'authorization': f"Bearer sk-XpP3t1urDRKvZmmLtRhNvsCDLoCkGfFRk5ihXWn6maLPuqzg"
        },
    )

    while True:
        if response.status_code == 202:
            print("Generation in-progress, try again in 10 seconds.")
            time.sleep(10)
        elif response.status_code == 200:
            print("Generation complete!")
            with open("video.mp4", 'wb') as file:
                file.write(response.content)
            break
        else:
            raise Exception(str(response.json()))


if __name__ == "__main__":
    image = '../test/test.png'
    video_id = image_to_video(image)
    if video_id:
        print(f"Video ID: {video_id}")
        get_video(video_id)
