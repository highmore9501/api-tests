import requests
import os
import time
from dotenv import load_dotenv

load_dotenv()
# 从.env文件中读取API Key
x_api_key = os.getenv("X_API_KEY")

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "x-api-key": x_api_key
}


def download_video(video_id):
    # 查询视频生成状态
    get_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"

    while True:
        try:
            response = requests.get(get_url, headers=headers)
            data = response.json()["data"]
            status = data['status']

            if status == "completed":
                video_url = data['video_url']
                # 下载视频并保存
                video_response = requests.get(video_url, headers=headers)
                outputFile = f"output/{video_id}_output.mp4"
                with open(outputFile, "wb") as f:
                    f.write(video_response.content)
                print(f"视频已保存到{outputFile}")
                break
            elif status == "failed":
                error = data['error']
                print(error["code"], error["detail"])
                break
            else:
                time.sleep(20)
        except:
            pass


if __name__ == "__main__":
    video_id = "2018e1de550646e3aceb855e84911b38"
    download_video(video_id)
