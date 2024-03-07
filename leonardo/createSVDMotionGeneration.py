# 这个api测试失败，具体内容见json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("LEONARDO_AI_API_KEY")

# 可以用户上传图片，或者调用之前生成的图片，或者经由图片变化再生成的图片来生成视频
image_id = "9fb4eab9-dd75-4ccf-bfcd-14636d8ac924"

url = "https://cloud.leonardo.ai/api/rest/v1/generations-motion-svd"

payload = {
    "imageId": image_id,
    "isPublic": False,
    "isInitImage": False,
    "isVariation": False,
    "motionStrength": 5
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {api_key}"
}

response = requests.post(url, json=payload, headers=headers)

fileName = 'createSVDMotionGeneration.json'

with open(f"./responses/{fileName}", 'w') as f:
    f.write(response.text)
