# 这个功能是给3d模型添加皮肤，所以需要有一个modelAssetId，也就是已经上传的模型的id

import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("LEONARDO_AI_API_KEY")

url = "https://cloud.leonardo.ai/api/rest/v1/generations-texture"

payload = {
    "prompt": "the ground of the snow-capped mountain",
    "modelAssetId": "16e7060a-803e-4df3-97ee-edcfa5dc9cc8",
    "preview": True
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {api_key}"
}

response = requests.post(url, json=payload, headers=headers)

fileName = 'createTexture.json'

with open(f"./responses/{fileName}", 'w') as f:
    f.write(response.text)
