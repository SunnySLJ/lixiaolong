import requests
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Token (从浏览器获取)
token = "71aa646a-d1a4-4027-8d68-bb25512ba062"

# 使用本地图片的 URL（先复制到图床或使用已有 URL）
# 或者使用空 imageUrls 测试
prompt = "春分龙抬头天文奇观，漆黑夜空中春分与龙抬头天象重合，光芒四射，星辰变换，龙形光影与星辰交融，祥瑞之兆，神龙现身"
base_url = "https://aihuanying.com/prod-api"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "token": token,
    "Authorization": token,
    "User-Agent": "Mozilla/5.0",
}

print("=" * 60)
print("帧龙虾视频生成 API")
print("=" * 60)

# 测试视频生成接口
payload = {
    "prompt": prompt,
    "imageUrls": [],  # 先不传图片测试
    "aspectRatio": "9:16",
    "videoRatio": "9:16",
    "ratio": "9:16",
    "duration": 10,
    "quality": "standard"
}

print(f"\n提示词：{prompt[:50]}...")
print(f"比例：9:16")
print(f"时长：10 秒")

try:
    resp = requests.post(
        f"{base_url}/api/v1/aiMediaGenerations/generateVideo",
        json=payload,
        headers=headers,
        timeout=180,
        verify=False
    )
    
    print(f"\nHTTP 状态码：{resp.status_code}")
    result = resp.json()
    
    print("=" * 60)
    print("API 响应:")
    print("=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("=" * 60)
    
    if result.get("code") == 200:
        data = result.get("data", {})
        print(f"\n✓ 任务已提交！")
        print(f"任务 ID: {data.get('taskId')}")
        print(f"状态：{data.get('status')}")
        if data.get("videoUrl"):
            print(f"视频 URL: {data.get('videoUrl')}")
        else:
            print("视频正在生成中...")
    else:
        print(f"\n✗ 失败：{result.get('msg')}")
        print(f"错误码：{result.get('code')}")
        
except Exception as e:
    print(f"请求失败：{e}")
