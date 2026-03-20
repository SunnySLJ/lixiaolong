import requests
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Token (从浏览器获取)
token = "71aa646a-d1a4-4027-8d68-bb25512ba062"

cover_path = r"C:\Users\爽爽\Desktop\图片\cover.jpg"
prompt = "春分龙抬头天文奇观，漆黑夜空中春分与龙抬头天象重合，光芒四射，星辰变换，龙形光影与星辰交融，祥瑞之兆，神龙现身"
base_url = "https://aihuanying.com/prod-api"

print("=" * 60)
print("帧龙虾 API 视频生成")
print("=" * 60)

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "token": token,
    "Authorization": token,
    "User-Agent": "Mozilla/5.0",
}

# 1. 上传封面
print(f"\nStep 1: 上传封面图片...")
try:
    with open(cover_path, "rb") as f:
        files = {"file": ("cover.jpg", f, "image/jpeg")}
        resp = requests.post(
            f"{base_url}/api/v1/files/upload",
            files=files,
            headers=headers,
            timeout=30,
            verify=False
        )
        print(f"HTTP: {resp.status_code}")
        result = resp.json()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        file_url = result.get("data", {}).get("url")
        if not file_url:
            print(f"上传失败：{result.get('msg')}")
            exit(1)
        print(f"文件 URL: {file_url}")
except Exception as e:
    print(f"上传失败：{e}")
    exit(1)

# 2. 生成视频
print(f"\nStep 2: 提交视频生成任务...")
payload = {
    "prompt": prompt,
    "imageUrls": [file_url],
    "ratio": "9:16",
    "duration": 10,
    "quality": "standard"
}

try:
    resp = requests.post(
        f"{base_url}/api/v1/aiMediaGenerations/generateVideo",
        json=payload,
        headers=headers,
        timeout=180,
        verify=False
    )
    print(f"HTTP: {resp.status_code}")
    result = resp.json()
    
    print("=" * 60)
    print("API 响应:")
    print("=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("=" * 60)
    
    if result.get("code") == 200:
        data = result.get("data", {})
        print(f"\n任务 ID: {data.get('taskId')}")
        print(f"状态：{data.get('status')}")
        if data.get("videoUrl"):
            print(f"视频 URL: {data.get('videoUrl')}")
        else:
            print("视频正在生成中...")
    else:
        print(f"失败：{result.get('msg')}")
        
except Exception as e:
    print(f"请求失败：{e}")
