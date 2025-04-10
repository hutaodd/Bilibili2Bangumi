import requests
import json
import time  # 添加time模块导入

def add_to_collection(subject_id, types, bgm_token):
    url = f'https://api.bgm.tv/v0/users/-/collections/{subject_id}'
    headers = {
        'accept': '*/*',
        'Authorization': f'Bearer {bgm_token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Bilibili2Bangumi/1.0 (https://github.com/hutaodd/Bilibili2Bangumi)'
    }
    data = {
        'type': types  # 3=在看
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 204:
            print(f"ID {subject_id} 已成功添加到追番")
        elif response.status_code == 202:
            print(f"ID {subject_id} 请求已接受，正在处理")
        else:
            response.raise_for_status()
            
    except requests.exceptions.RequestException as e:
        print(f"ID {subject_id} 请求失败:", str(e))
        if hasattr(e, 'response') and e.response is not None:
            print("错误详情:", e.response.text)

def run(filename,types, bgm_token: str):
    # 读取ids文件
    with open(filename, 'r', encoding='utf-8') as f:
        ids_data = json.load(f)
    
    # 遍历所有ID
    for subject_id in ids_data['ids']:
        add_to_collection(subject_id, types, bgm_token)
        time.sleep(1)  # 添加延迟避免请求过快

if __name__ == "__main__":
    run('ids_1.json',1)
    run('ids_2.json',2)
    run('ids_3.json',3)
