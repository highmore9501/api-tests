import json
import base64
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("LEONARDO_AI_API_KEY")

url = "https://cloud.leonardo.ai/api/rest/v1/generations-lcm"

# 用图片和prompt生成lcm图片，效果不怎么样，是直接返回图片数据，不是返回图片id
# 参考的图片还不能太大，不然会返回 `imageDataUrl too long, max length of BASE64 is 1048576`
image_path = './images/a228bb08-c8ec-4bef-8c56-7d353ebcf3d5.jpg'
prompt = "A standing female swordsman with white hair, looking to the side. She is wearing a white dress and holding a sword. She has a serious expression."

# 读取image_path，并将之转化为base64编码
with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

encoded_string_len = len(encoded_string)

if encoded_string.startswith("data:image/jpeg;base64,") and encoded_string_len <= 1048576:
    print("encoded_string is good. ")
elif encoded_string_len <= 1048576:
    encoded_string = "data:image/jpeg;base64," + encoded_string
elif encoded_string_len > 1048576:
    print("encoded_string too long, max length of BASE64 is 1048576")
    print(f"encoded_string length: {encoded_string_len}")
    exit()

payload = {
    "width": 512,
    "height": 512,
    "prompt": prompt,
    "guidance": 8,
    "style": "ANIME",
    "steps": 15,
    "imageDataUrl": encoded_string
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {api_key}"
}

response = requests.post(url, json=payload, headers=headers)


fileName = 'createLCMGeneration'

with open(f"./responses/{fileName}.json", 'w') as f:
    f.write(response.text)

content = json.loads(response.text)

# 读取返回的json
imageDataUrl = content['lcmGenerationJob']['imageDataUrl'][0]

# 读取其中的图片按base64编码保存
imageDataUrl = imageDataUrl.split(",")[1]
imageDataUrl = imageDataUrl.encode()
with open(f"./responses/{fileName}.jpg", 'wb') as f:
    f.write(base64.decodebytes(imageDataUrl))
