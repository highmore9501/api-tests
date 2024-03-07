import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_host = f'https://api.stability.ai'
url = f"{api_host}/v1/user/account"

api_key = os.getenv("STABILITY_API_KEY")
if api_key is None:
    raise Exception("Missing Stability API key.")

response = requests.get(url, headers={
    'Accept': 'application/json',
    "Authorization": f"Bearer {api_key}"
})

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

# Do something with the payload...
payload = response.json()

print(payload)
