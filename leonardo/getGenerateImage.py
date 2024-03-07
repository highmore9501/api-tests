import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("LEONARDO_AI_API_KEY")

image_id = "c369a970-6010-4f99-9408-8105ab6107b8"

url = f"https://cloud.leonardo.ai/api/rest/v1/generations/{image_id}"

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)

fileName = 'getGenerateImage.json'

with open(f"./responses/{fileName}", 'w') as f:
    f.write(response.text)
