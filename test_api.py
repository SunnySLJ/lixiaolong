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

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "token": token,
    "Authorization": token,
    "User-Agent": "Mozilla/5.0",
}

print("=" * 60)
print("帧龙虾 API 测试")
print("=" * 60)

# 测试不同的上传 API 路径
upload_paths = [
    "/api/v1/files/upload",
    "/api/v1/file/upload",
    "/api/v1/upload",
    "/file/upload",
    "/upload",
    "/api/upload",
]

print(f"\n测试上传 API 路径...")
with open(cover_path, "rb") as f:
    files = {"file": ("cover.jpg", f, "image/jpeg")}
    
    for path in upload_paths:
        try:
            resp = requests.post(
                f"{base_url}{path}",
                files=files,
                headers=headers,
                timeout=10,
                verify=False
            )
            print(f"\n{path}: HTTP {resp.status_code}")
            if resp.status_code == 200:
                result = resp.json()
                print(json.dumps(result, ensure_ascii=False, indent=2))
                
                # 检查是否成功
                file_url = result.get("data", {}).get("url") or result.get("url")
                if file_url:
                    print(f"\n✓ 成功！文件 URL: {file_url}")
                    # 保存成功的配置
                    with open("C:\\Users\\爽爽\\.openclaw\\workspace\\aihuanying_config.json", "w") as cf:
                        json.dump({
                            "token": token,
                            "upload_path": path,
                            "file_url": file_url
                        }, cf, ensure_ascii=False, indent=2)
                    break
        except Exception as e:
            print(f"  错误：{e}")

print("\n" + "=" * 60)
