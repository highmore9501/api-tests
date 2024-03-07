import requests
import os
from dotenv import load_dotenv

url = "https://api.heygen.com/v1/avatar.list"

load_dotenv()
# 从.env文件中读取API Key
x_api_key = os.getenv("X_API_KEY")

headers = {
    "accept": "application/json",
    "x-api-key": x_api_key
}

response = requests.get(url, headers=headers)

avatar_list_file = "output/avatar_list.json"

with open(avatar_list_file, "w") as f:
    f.write(response.text)
