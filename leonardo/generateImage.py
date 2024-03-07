import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("LEONARDO_AI_API_KEY")
prompt = "An hippo riding a motorcycle."


url = "https://cloud.leonardo.ai/api/rest/v1/generations"

payload = {
    "height": 512,
    "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
    "prompt": prompt,
    "width": 512
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {api_key}"
}

response = requests.post(url, json=payload, headers=headers)

fileName = 'generateImage.json'

with open(f"./responses/{fileName}", 'w') as f:
    f.write(response.text)
