"""
直接从浏览器获取 cookie 并调用帧龙虾 API
"""
import requests
import json
import os
import time
import sys

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

# 配置
cover_path = r"C:\Users\爽爽\Desktop\图片\cover.jpg"
prompt = "春分龙抬头天文奇观，漆黑夜空中春分与龙抬头天象重合，光芒四射，星辰变换，龙形光影与星辰交融，祥瑞之兆，神龙现身"
base_url = "https://aihuanying.com/prod-api"

print("=" * 60)
print("帧龙虾 API 视频生成")
print("=" * 60)

# 从浏览器获取 cookie - 需要用户手动复制
print("\n请从浏览器获取 Token:")
print("1. 打开 https://aihuanying.com/")
print("2. 按 F12 打开开发者工具")
print("3. 在 Console 中执行：console.log(localStorage.getItem('token') || document.cookie)")
print("4. 复制 Token 值")
print()

# 尝试使用已保存的 token
token_file = "C:\\Users\\爽爽\\.openclaw\\workspace\\aihuanying_token.txt"
token = None

if os.path.exists(token_file):
    with open(token_file, 'r', encoding='utf-8') as f:
        token = f.read().strip()
        print(f"✓ 使用已保存的 Token: {token[:20]}...")
else:
    print("⚠ 未找到保存的 Token，需要手动提供")
    print(f"请将 Token 保存到：{token_file}")
    # 暂时使用空 token 测试
    token = ""

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
}

if token:
    # 尝试不同的 token 格式
    if token.startswith("Bearer "):
        headers["Authorization"] = token
    elif token.startswith("eyJ"):
        headers["Authorization"] = f"Bearer {token}"
    else:
        headers["token"] = token
        headers["Authorization"] = f"Bearer {token}"

# 1. 上传封面图片
print(f"\nStep 1: 上传封面图片...")
print(f"文件：{cover_path}")

if not os.path.exists(cover_path):
    print("✗ 文件不存在")
    exit(1)

try:
    with open(cover_path, 'rb') as f:
        files = {'file': ('cover.jpg', f, 'image/jpeg')}
        
        resp = requests.post(
            f"{base_url}/api/v1/files/upload",
            files=files,
            headers=headers,
            timeout=30,
            verify=False
        )
        
        print(f"HTTP 状态码：{resp.status_code}")
        upload_result = resp.json()
        print(f"上传结果：{json.dumps(upload_result, ensure_ascii=False)}")
        
        # 获取文件 URL
        file_url = None
        if upload_result.get('code') == 200:
            file_url = upload_result.get('data', {}).get('url')
        elif upload_result.get('success'):
            file_url = upload_result.get('data', {}).get('url')
        
        if not file_url:
            msg = upload_result.get('msg') or upload_result.get('message', '未知错误')
            print(f"✗ 上传失败：{msg}")
            if "登录" in msg:
                print("\n需要登录！请：")
                print("1. 在浏览器中登录 https://aihuanying.com/")
                print("2. 按 F12 打开开发者工具")
                print("3. 在 Application > Local Storage 中找到 'token'")
                print("4. 复制 token 值并保存到：C:\\Users\\爽爽\\.openclaw\\workspace\\aihuanying_token.txt")
            exit(1)
        
        print(f"✓ 文件 URL: {file_url}")
        
except requests.exceptions.SSLError:
    print("✗ SSL 错误，尝试禁用验证...")
except Exception as e:
    print(f"✗ 上传失败：{e}")
    exit(1)

# 2. 调用视频生成 API
print("\nStep 2: 提交视频生成任务...")
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
    
    print(f"HTTP 状态码：{resp.status_code}")
    result = resp.json()
    
    print("=" * 60)
    print("API 响应:")
    print("=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("=" * 60)
    
    # 解析结果
    if result.get('code') == 200 or result.get('success'):
        data = result.get('data', result)
        task_id = data.get('taskId') or data.get('task_id') or data.get('id')
        status = data.get('status')
        video_url = data.get('videoUrl') or data.get('video_url')
        
        print(f"\n✓ 视频任务已提交！")
        print(f"任务 ID: {task_id}")
        print(f"状态：{status}")
        if video_url:
            print(f"视频 URL: {video_url}")
        else:
            print(f"视频正在生成中，请稍后查询...")
    else:
        msg = result.get('message') or result.get('msg') or result.get('error', '未知错误')
        print(f"\n✗ 视频生成失败：{msg}")
        
except Exception as e:
    print(f"请求失败：{e}")
