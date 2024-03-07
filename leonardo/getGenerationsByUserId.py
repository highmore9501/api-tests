import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("LEONARDO_AI_API_KEY")
user_id = "b5df4a4f-7898-43ef-8c9e-b53785b7ddde"
url = f"https://cloud.leonardo.ai/api/rest/v1/generations/user/{user_id}"

headers = {
    "accept": "application/json",
    "authorization": f"Bearer {api_key}"
}

response = requests.get(url, headers=headers)

fileName = 'getGenerationsByUserId.json'

with open(f"./responses/{fileName}", 'w') as f:
    f.write(response.text)
