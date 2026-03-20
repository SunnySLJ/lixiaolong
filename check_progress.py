import requests
import json
import os
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

# Token
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
print("帧龙虾视频生成进度查询")
print("=" * 60)

# 使用 pageList 接口查询
payload = {
    "pageNum": 1,
    "pageSize": 10,
    "generateStatus": ""  # 可以过滤状态
}

print(f"正在查询视频列表...")
print(f"API: {base_url}/api/v1/aiMediaGenerations/pageList")

try:
    resp = requests.post(
        f"{base_url}/api/v1/aiMediaGenerations/pageList",
        json=payload,
        headers=headers,
        timeout=30,
        verify=False
    )
    
    print(f"HTTP: {resp.status_code}")
    result = resp.json()
    
    print("=" * 60)
    print("API 响应:")
    print("=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("=" * 60)
    
    if result.get("code") == 0 or result.get("code") == 200:
        data = result.get("data", {})
        records = data.get("records", []) or data.get("list", [])
        
        if records:
            print(f"\n找到 {len(records)} 个视频任务")
            
            # 查找最近的任务
            latest_video = records[0]
            group_no = latest_video.get("groupNo")
            status = latest_video.get("generateStatus") or latest_video.get("status")
            video_url = latest_video.get("videoUrl") or latest_video.get("url")
            prompt = latest_video.get("prompt", "")[:50]
            
            print(f"\n最新任务:")
            print(f"  编号：{group_no}")
            print(f"  状态：{status}")
            print(f"  提示词：{prompt}...")
            print(f"  视频 URL: {video_url}")
            
            if status == "SUCCESS" or status == "COMPLETED" or (video_url and status not in ["PROCESSING", "PENDING", "FAILED"]):
                print("\n✓ 视频已生成完成！")
                
                if video_url:
                    print(f"\n正在下载视频...")
                    video_filename = f"春分龙抬头_{group_no}.mp4"
                    video_path = os.path.join(output_dir, video_filename)
                    
                    video_resp = requests.get(video_url, stream=True, timeout=300, verify=False)
                    video_resp.raise_for_status()
                    
                    with open(video_path, "wb") as f:
                        for chunk in video_resp.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    file_size = os.path.getsize(video_path)
                    print(f"✓ 视频已下载：{video_path}")
                    print(f"文件大小：{file_size / 1024 / 1024:.2f} MB")
                    
                    # 保存视频路径供下一步使用
                    with open(os.path.join(output_dir, "latest_video.txt"), "w", encoding="utf-8") as f:
                        f.write(video_path)
                    
                    print(f"\n视频已保存到：{video_path}")
                else:
                    print(f"\n视频仍在生成中，当前状态：{status}")
                    print("请稍后重试...")
            else:
                print(f"\n视频仍在生成中，当前状态：{status}")
                print("请稍后重试...")
        else:
            print("\n暂无视频记录")
    else:
        print(f"\n查询失败：{result.get('msg')}")
        
except Exception as e:
    print(f"请求失败：{e}")

print("=" * 60)
