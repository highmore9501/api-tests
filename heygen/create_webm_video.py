import requests
import os
from dotenv import load_dotenv
from download_video import download_video
from add_caption import get_caption_video_id, download_caption_video

load_dotenv()
# 从.env文件中读取API Key
x_api_key = os.getenv("X_API_KEY")

input_text = """
2月25日，记者从海南省消防救援总队获悉，海南持续开展消防安全除患攻坚行动，连日来，全省各地消防救援机构在检查中发现一些单位存在不同程度的消防安全隐患，对第二批火灾隐患单位进行曝光，此次共曝光消防隐患单位27家。

消防救援部门在检查中发现，万宁长丰望金河宾馆，室内消火栓系统无水、无法正常使用，场所内疏散指示标志损坏率超过50%，宾馆客房外窗违规设置影响逃生和灭火救援的障碍物，综合判定为重大火灾隐患单位；此外，东方四更嘉佳假日旅租、乐东黎族自治县抱由镇卡酷七色光幼儿园、五指山百货大楼等26家单位，因存在公共娱乐场所未按照国家工程建设消防技术标准设置火灾自动报警系统，儿童活动场所所在楼层设置不符合国家工程建设消防技术标准的规定，违规停放电动自行车等消防违法行为，被依法下达整改通知书，责令立即或限期整改。
"""

generate_url = "https://api.heygen.com/v1/video.generate"

url = "https://api.heygen.com/v1/video.webm"

payload = {
    "avatar_pose_id": "Wilson-insuit-20220722",
    "avatar_style": "normal",
    "input_text": input_text,
    "voice_id": "961546a1be64458caa1386ff63dd5d5f"
}
headers = {
    "accept": "application/json",
    "x-api-key": x_api_key,
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

video_id = response.json()["data"]["video_id"]
print(video_id)

# 下载并保存视频:无字幕
download_video(video_id)

# 如果想要下载并保存有字幕的视频，可以使用下面的语句
# add_caption_video_id = get_caption_video_id(video_id)
# download_caption_video(add_caption_video_id)
# 4de6397982414226a81f708e3b87241a
