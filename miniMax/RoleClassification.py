import os
from dotenv import load_dotenv
import requests
load_dotenv()

group_id = os.environ.get("MINI_MAX_GROUP_ID")
api_key = os.environ.get("MINI_MAX_API_KEY")

# 上传文档，拿到文档file_id
url = f'https://api.minimax.chat/v1/files/upload?GroupId={group_id}'
uploadHeaders = {
    'authority': 'api.minimax.chat',
    'Authorization': f'Bearer {api_key}'
}

data = {
    'purpose': 'retrieval'
}

files = {
    'file': open('/Users/minimax/Downloads/export_file (1).csv', 'rb')
}

response = requests.post(url, headers=uploadHeaders, data=data, files=files)
print(response.text)

file_id = response.json()['file_id']

# 触发角色识别任务
url = f'https://api.minimax.chat/v1/role_recognition/task/async/crun?GroupId=${group_id}&file_id=${file_id}'

headers = {
    'Authorization': f'Bearer ${api_key}'
}

response = requests.post(url, headers=headers)
print(response.text)

task_id = response.json()['task']['task_id']

# 查询任务状态
url = f'https://api.minimax.chat/v1/role_recognition/task/retrieve?GroupId=${group_id}&task_id=${task_id}'

headers = {
    'Authorization': f'Bearer ${api_key}'
}

response = requests.get(url, headers=headers)
print(response.text)
status_msg = response.json()['base_resp']['status_msg']


# 如果执行成功，读取结果
if status_msg == 'success':
    #
    url = f"https://api.minimax.chat/v1/files/retrieve_content?GroupId={group_id}&file_id=87402838655043"

    headers = {
        'content-type': 'application/json',
        'Authorization': 'Bearer ${api_key}'
    }

    response = requests.get(url, headers=headers)
    print(response.text)
