import json
import os
from dotenv import load_dotenv
import requests
load_dotenv()

group_id = os.environ.get("MINI_MAX_GROUP_ID")
api_key = os.environ.get("MINI_MAX_API_KEY")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}


class BaseError(Exception):
    msg = ""

    def __init__(self, msg):
        super().__init__(self)
        self.msg = msg


def create_assistant():
    url = f"https://api.minimax.chat/v1/assistants/create?GroupId={group_id}"
    payload = json.dumps({
        "model": "abab6-chat",
        "name": "新闻记者",
        "description": "新闻记者，用于咨询各类新闻",
        "instructions": "是一个新闻记者，擅长解答关于新闻的各类问题",
        "tools": [
            {
                "type": "web_search"
            }
        ]
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
        raise BaseError(response.status_msg)
    data = json.loads(response.text)
    if data["base_resp"]["status_code"] != 0:
        raise BaseError(data["base_resp"]["status_msg"])
    return data["id"]


def create_thread():
    url = f"https://api.minimax.chat/v1/threads/create?GroupId={group_id}"
    payload = json.dumps({})
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code != 200:
        raise BaseError(response.status_msg)
    data = json.loads(response.text)
    if data["base_resp"]["status_code"] != 0:
        raise BaseError(data["base_resp"]["status_msg"])
    return data["id"]


def create_run_stream(assistant_id, thread_id, content):
    url = f"https://api.minimax.chat/v1/threads/run/create_stream?GroupId={group_id}"
    payload = json.dumps({
        "stream": 2,
        "thread_id": thread_id,
        "assistant_id": assistant_id,
        "messages": [
            {
                "type": 2,
                "role": "user",
                "content": content  # 这里填写hex编码格式的音频内容
            }
        ],
        "model": "abab6-chat",
        "t2a_option": {
            "model": "speech-01",
            "voice_id": "male-qn-qingse"
        },
        "tools": [
            {
                "type": "web_search"
            }
        ]
    })

    audio_contents = {}

    response = requests.request(
        "POST", url, headers=headers, data=payload, stream=True)
    if response.status_code != 200:
        raise BaseError(response.status_msg)
    for chunk in response.raw:
        chunk = chunk.decode("utf-8")
        if chunk.startswith("data: "):
            print(chunk)
            data = json.loads(chunk[6:])
            if "status_code" in data["base_resp"] and data["base_resp"]["status_code"] != 0:
                raise BaseError(data["base_resp"]["status_msg"])
            if data["data"]["object"] == "message" and data["data"]["role"] == "ai":
                for content in data["data"]["content"]:
                    if "audio_file" in content and "value" in content["audio_file"]:
                        if content["id"] not in audio_contents:
                            audio_contents[content["id"]] = ""
                        audio_contents[content["id"]
                                       ] += content["audio_file"]["value"]
            if "status_code" in data["base_resp"] and data["base_resp"]["status_code"] == 0:
                return audio_contents
        elif chunk != "\n":
            data = json.loads(chunk)
            raise BaseError(data["base_resp"]["status_msg"])


def mp3_to_hex(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        hex_content = file_content.hex()
    return hex_content


def main(video_file):
    # 把video_file改成hex编码的文本，这个方法没写
    content = mp3_to_hex(video_file)
    try:
        assistant_id = create_assistant()
        print("assistant id:" + assistant_id)
        thread_id = create_thread()
        print("thread id:" + thread_id)
        audio_contents = create_run_stream(assistant_id, thread_id, content)
        index = 0
        for audio_content in audio_contents.values():
            audio = bytes.fromhex(audio_content)
            filename = "temp_" + str(index) + ".mp3"
            with open(filename, "wb") as file:
                index += 1
                file.write(audio)
        print("end")

    except BaseError as e:
        print("error: " + e.msg)
    except Exception:
        print("unkonwn error")
        exit(1)


if __name__ == "__main__":
    video_file = input("请输入要转换成文字的音频文件路径:")
    main(video_file)
