import requests
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

token = "71aa646a-d1a4-4027-8d68-bb25512ba062"
base_url = "https://aihuanying.com/prod-api"
output_dir = "S:\\ruoyi\\video"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "token": token,
    "Authorization": token,
    "User-Agent": "Mozilla/5.0",
}

os.makedirs(output_dir, exist_ok=True)

print("=" * 60)
print("下载已生成的视频")
print("=" * 60)

# 查询视频列表
payload = {"pageNum": 1, "pageSize": 10}

resp = requests.post(
    f"{base_url}/api/v1/aiMediaGenerations/pageList",
    json=payload,
    headers=headers,
    timeout=30,
    verify=False
)

result = resp.json()

if result.get("code") == 0:
    records = result.get("data", [])
    
    if records:
        # 获取最新视频（第一个）
        latest = records[0]
        group_no = latest.get("groupNo")
        status = latest.get("status")
        media_url = latest.get("mediaUrl")
        prompt = latest.get("prompt", "")[:50]
        
        print(f"\n视频信息:")
        print(f"  编号：{group_no}")
        print(f"  状态：{status}")
        print(f"  提示词：{prompt}...")
        print(f"  媒体 URL: {media_url}")
        
        # 状态 1 表示完成
        if status == 1 and media_url:
            print(f"\n✓ 视频已生成完成，正在下载...")
            
            video_filename = f"春分龙抬头_{group_no}.mp4"
            video_path = os.path.join(output_dir, video_filename)
            
            # 下载视频
            video_resp = requests.get(media_url, stream=True, timeout=300, verify=False)
            video_resp.raise_for_status()
            
            with open(video_path, "wb") as f:
                for chunk in video_resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            file_size = os.path.getsize(video_path)
            print(f"\n✓ 视频已下载：{video_path}")
            print(f"文件大小：{file_size / 1024 / 1024:.2f} MB")
            
            # 保存路径
            with open(os.path.join(output_dir, "latest_video.txt"), "w", encoding="utf-8") as f:
                f.write(video_path)
            
            print(f"\n视频路径：{video_path}")
        else:
            print(f"\n视频尚未完成，状态：{status}")
    else:
        print("\n暂无视频记录")
else:
    print(f"\n查询失败：{result.get('msg')}")

print("=" * 60)
