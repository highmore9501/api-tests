import requests
import os
from dotenv import load_dotenv

load_dotenv()
x_api_key = os.getenv("X_API_KEY")

url = "https://api.heygen.com/v1/voice.list"

headers = {
    "accept": "application/json",
    "x-api-key": x_api_key
}

response = requests.get(url, headers=headers)

voice_list_file = "output/voice_list.json"

with open(voice_list_file, "w") as f:
    f.write(response.text)
