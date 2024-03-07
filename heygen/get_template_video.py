import requests
import os
from dotenv import load_dotenv

load_dotenv()
# 从.env文件中读取API Key
x_api_key = os.getenv("X_API_KEY")

# 已有视频的id
video_id = "16ddb45a27a745928e2ee7e8576ca6b1"

url = f"https://api.heygen.com/v1/template.get?video_id={video_id}"

headers = {
    "accept": "application/json",
    "x-api-key": x_api_key
}
# 根据已生成的视频id获取模板id
response = requests.get(url, headers=headers)

print(response.text)

template_id = response.json()["data"]["template_id"]
print(f"模板id为{template_id}")
