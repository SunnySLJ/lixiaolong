"""
直接调用帧龙虾 API 生成视频
POST https://aihuanying.com/prod-api/api/v1/aiMediaGenerations/generateVideo
"""
import requests
import json
import sys
import os
import time
import http.cookiejar
import urllib.request

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

# 配置
cover_path = r"C:\Users\爽爽\Desktop\图片\cover.jpg"
prompt = "春分龙抬头天文奇观，漆黑夜空中春分与龙抬头天象重合，光芒四射，星辰变换，龙形光影与星辰交融，祥瑞之兆，神龙现身"
base_url = "https://aihuanying.com/prod-api"

print("=" * 60)
print("帧龙虾 API 视频生成")
print("=" * 60)
print(f"封面：{cover_path}")
print(f"提示词：{prompt[:50]}...")
print()

# 检查文件
if not os.path.exists(cover_path):
    print(f"错误：封面图片不存在")
    sys.exit(1)

# 创建带 cookie 的 opener (禁用 SSL 验证)
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cookie_jar),
    urllib.request.HTTPSHandler(context=ctx)
)
opener.addheaders = [
    ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'),
    ('Accept', 'application/json, text/plain, */*'),
    ('Accept-Language', 'zh-CN,zh;q=0.9'),
]

# 1. 先访问主页获取 cookie
print("Step 1: 获取登录状态...")
try:
    opener.open("https://aihuanying.com/", timeout=10)
    print(f"✓ 已获取 {len(cookie_jar)} 个 cookies")
    
    # 打印 cookies
    for cookie in cookie_jar:
        if "token" in cookie.name.lower() or "auth" in cookie.name.lower() or "session" in cookie.name.lower():
            print(f"  认证 cookie: {cookie.name}={cookie.value[:50]}...")
except Exception as e:
    print(f"获取 cookie 失败：{e}")

# 2. 上传封面图片
print("\nStep 2: 上传封面图片...")
try:
    with open(cover_path, 'rb') as f:
        boundary = "----WebKitFormBoundary" + str(int(time.time() * 1000))
        
        # 构建 multipart 请求
        body = []
        body.append(f"--{boundary}".encode())
        body.append(b'Content-Disposition: form-data; name="file"; filename="cover.jpg"')
        body.append(b'Content-Type: image/jpeg')
        body.append(b'')
        body.append(f.read())
        body.append(f"--{boundary}--".encode())
        body.append(b'')
        
        body_data = b"\r\n".join(body)
        
        req = urllib.request.Request(
            f"{base_url}/api/v1/files/upload",
            data=body_data,
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
            method="POST"
        )
        
        resp = opener.open(req, timeout=30)
        upload_result = json.loads(resp.read().decode('utf-8'))
        
        print(f"上传结果：{json.dumps(upload_result, ensure_ascii=False)}")
        
        # 获取文件 URL
        file_url = None
        if upload_result.get('code') == 200:
            file_url = upload_result.get('data', {}).get('url')
        elif upload_result.get('success'):
            file_url = upload_result.get('data', {}).get('url') or upload_result.get('url')
        
        if not file_url:
            print("✗ 未获取到文件 URL")
            sys.exit(1)
        
        print(f"✓ 文件 URL: {file_url}")
        
except Exception as e:
    print(f"上传失败：{e}")
    sys.exit(1)

# 3. 调用视频生成 API
print("\nStep 3: 提交视频生成任务...")
payload = {
    "prompt": prompt,
    "imageUrls": [file_url],
    "ratio": "9:16",
    "duration": 10,
    "quality": "standard"
}

try:
    req = urllib.request.Request(
        f"{base_url}/api/v1/aiMediaGenerations/generateVideo",
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "Content-Type": "application/json",
        },
        method="POST"
    )
    
    resp = opener.open(req, timeout=180)
    result = json.loads(resp.read().decode('utf-8'))
    
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
            print(f"视频正在生成中...")
    else:
        print(f"\n✗ 视频生成失败：{result.get('message') or result.get('msg')}")
        
except urllib.error.HTTPError as he:
    err_body = he.read().decode('utf-8', errors='replace')
    print(f"HTTP 错误 {he.code}: {err_body}")
except Exception as e:
    print(f"请求失败：{e}")
