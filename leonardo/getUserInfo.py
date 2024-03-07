import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("LEONARDO_AI_API_KEY")

url = "https://cloud.leonardo.ai/api/rest/v1/me"

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)

fileName = 'getUserInfo.json'

with open(f"./responses/{fileName}", 'w') as f:
    f.write(response.text)
