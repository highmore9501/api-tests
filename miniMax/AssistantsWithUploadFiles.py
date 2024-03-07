import time
import json
import os
from dotenv import load_dotenv
import requests
load_dotenv()

group_id = os.environ.get("MINI_MAX_GROUP_ID")
api_key = os.environ.get("MINI_MAX_API_KEY")

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}
headers_retrieval = {
    'Authorization': f'Bearer {api_key}',
    'authority': 'api.minimax.chat',
}


# 流程零：上传文档
def create_file():
    url = f"https://api.minimax.chat/v1/files/upload?GroupId={group_id}"
    data = {
        'purpose': 'assistants'
    }

    files = {
        'file': open('./倚天屠龙记.txt', 'rb')
    }
    response = requests.post(
        url, headers=headers_retrieval, data=data, files=files)
    return response.json()

# 流程一：创建助手


def create_assistant(file_id):
    url = f"https://api.minimax.chat/v1/assistants/create?GroupId={group_id}"
    payload = json.dumps({
        "model": "abab5.5-chat",  # 模型版本，目前支持abab6-chat和abab5.5-chat
        "name": "小说专家",  # 助手名称
        "description": "小说专家，用在小说解读场景中回答用户问题",  # 助手描述
        # 助手设定（即bot_setting)
        "instructions": "是一个小说专家，读过万卷书，了解小说里的各种细致情节，另外也非常热心，会热情的帮读者解答小说里的问题",
        "file_ids": [
            str(file_id)
        ],
        "tools": [{"type": "retrieval"}]

    })
    response = requests.post(url, headers=headers, data=payload)
    return response.json()

# 流程二：创建线程


def create_thread():
    url = f"https://api.minimax.chat/v1/threads/create?GroupId={group_id}"
    response = requests.post(url, headers=headers)
    return response.json()

# 流程三：往线程里添加信息


def add_message_to_thread(thread_id):
    url = f"https://api.minimax.chat/v1/threads/messages/add?GroupId={group_id}"
    payload = json.dumps({
        "thread_id": thread_id,
        "role": "user",
        "content": "在倚天屠龙记中，无俗念词的作者是谁？",
    })
    response = requests.post(url, headers=headers, data=payload)
    return response.json()

# 流程四：使用助手处理该线程


def run_thread_with_assistant(thread_id, assistant_id):
    # 创建assistants进行向量化以及存储时需要一定的时间，可以考虑使用retrieve assistant检索是否创建成功
    time.sleep(200)
    url = f"https://api.minimax.chat/v1/threads/run/create?GroupId={group_id}"
    payload = json.dumps({
        "thread_id": thread_id,
        "assistant_id": assistant_id
    })
    response = requests.post(url, headers=headers, data=payload)
    return response.json()

# 流程五：获取线程中助手处理出的新信息


def get_thread_messages(thread_id):
    url = f"https://api.minimax.chat/v1/threads/messages/list?GroupId={group_id}"
    payload = json.dumps({
        "thread_id": thread_id
    })
    response = requests.get(url, headers=headers, data=payload)
    return response.json()


def check_thread_run_status(thread_id, run_id):
    url = f"https://api.minimax.chat/v1/threads/run/retrieve?GroupId={group_id}"
    payload = json.dumps({
        "thread_id": str(thread_id),
        "run_id": str(run_id)
    })
    completed = False
    while not completed:
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            response_data = response.json()
            status = response_data.get('status', '')
            print(f"Status: {status}")
            if status == 'completed':
                completed = True
                print("Process completed, exiting loop.")
            else:
                time.sleep(2)  # 如果状态不是completed，等待两秒后重新请求
        else:
            print(f"Error: {response.status_code}")
            break  # 如果请求失败，退出循环
    return completed
# 主流程


def main():
    # 上传文档
    file_response = create_file()
    file_id = file_response.get('file', {}).get('file_id')
    print("file_id:", file_id)

    # 创建助手
    assistant_response = create_assistant(file_id)
    assistant_id = assistant_response.get('id', '')
    print("assistant_id:", assistant_id)

    # 创建线程
    thread_response = create_thread()
    thread_id = thread_response.get('id', '')
    print("thread_id:", thread_id)

    # 往线程里添加信息
    add_message_to_thread(thread_id)  # 不保存返回值

    # 使用助手处理该线程
    run_response = run_thread_with_assistant(thread_id, assistant_id)
    run_id = run_response.get('id', '')  # 假设run_response是正确的JSON响应，并包含run_id
    print("run_id:", run_id)

    # 检查助手处理状态
    if check_thread_run_status(thread_id, run_id):
        # 获取线程中助手处理出的新信息
        thread_messages_response = get_thread_messages(thread_id)
        # 打印JSON数据
        print(json.dumps(thread_messages_response, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
