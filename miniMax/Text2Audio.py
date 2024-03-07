import os
from dotenv import load_dotenv
import requests
load_dotenv()

group_id = os.environ.get("MINI_MAX_GROUP_ID")
api_key = os.environ.get("MINI_MAX_API_KEY")

url = f"https://api.minimax.chat/v1/text_to_speech?GroupId={group_id}"
headers = {"Authorization": f"Bearer {api_key}",
           "Content-Type": "application/json"}

if __name__ == "__main__":
    try:
        voice_select = input(
            "请输入要使用的语音id号码:\n1.male-qn-qingse\n2.female-shaonv\n3.female-yujie\n4.audiobook_male_2:")
        if voice_select == "1":
            voice_id = "male-qn-qingse"
        elif voice_select == "2":
            voice_id = "female-shaonv"
        elif voice_select == "3":
            voice_id = "female-yujie"
        elif voice_select == "4":
            voice_id = "audiobook_male_2"
        else:
            print("输入错误，请重新输入正确的语音id号码")
            exit()
    except Exception as e:
        print("输入错误，请重新输入正确的语音id号码")
        exit()

    sentence = input("请输入要转换成语音的文字:")
    data = {
        "voice_id": voice_id,
        # 如同时传入voice_id和timber_weights时，则会自动忽略voice_id，以timber_weights传递的参数为准
        "text": sentence,
        "model": "speech-01",
        "speed": 1.0,
        "vol": 1.0,
        "pitch": 0,
        # "timber_weights": [
        #     {
        #         "voice_id": "male-qn-qingse",
        #         "weight": 1
        #     },
        #     {
        #         "voice_id": "female-shaonv",
        #         "weight": 1
        #     },
        #     {
        #         "voice_id": "female-yujie",
        #         "weight": 1
        #     },
        #     {
        #         "voice_id": "audiobook_male_2",
        #         "weight": 1
        #     }
        # ]
    }

    response = requests.post(url, headers=headers, json=data)
    print("trace_id", response.headers.get("Trace-Id"))
    if response.status_code != 200 or "json" in response.headers["Content-Type"]:
        print("调用失败", response.status_code, response.text)
        exit()
    with open(f"{voice_id}_output.mp3", "wb") as f:
        f.write(response.content)
