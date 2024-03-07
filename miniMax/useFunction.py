import json
import os
from dotenv import load_dotenv
import requests
load_dotenv()

group_id = os.environ.get("MINI_MAX_GROUP_ID")
api_key = os.environ.get("MINI_MAX_API_KEY")
url = "https://api.minimax.chat/v1/text/chatcompletion_v2"

payload = json.dumps({
    "model": "abab5.5-chat",
    "messages": [
        {
            "role": "system",
            "content": "MM智能助理是一款由MiniMax自研的，没有调用其他产品的接口的大型语言模型。MiniMax是一家中国科技公司，一直致力于进行大模型相关的研究。"
        },
        {
            "role": "user",
            "content": "最近海口的天气怎么样？"
        }
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "获取进去某一地点的天气情况",
                "parameters": "{\"type\": \"object\", \"properties\": {\"location\": {\"type\": \"string\", \"description\": \"某一个城市，比如北京、上海\"}}, \"required\": [\"location\"]}"
            }
        }
    ],
    "tool_choice": "auto",
    "stream": True,
    "max_tokens": 10000,
    "temperature": 0.9,
    "top_p": 1
})
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
