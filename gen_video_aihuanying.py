import requests
import json
import sys
import os

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

# 封面图片路径
cover_path = r"C:\Users\爽爽\Desktop\图片\cover.jpg"

# 视频生成提示词（使用之前的文案）
prompt = "春分龙抬头天文奇观，漆黑夜空中春分与龙抬头天象重合，光芒四射，星辰变换，龙形光影与星辰交融，祥瑞之兆，神龙现身"

# API 端点
base_url = "https://aihuanying.com/prod-api"
upload_url = f"{base_url}/api/v1/aiMediaGenerations/generateVideo"

# 检查文件是否存在
if not os.path.exists(cover_path):
    print(f"错误：封面图片不存在：{cover_path}")
    sys.exit(1)

print("=" * 60)
print("正在调用帧龙虾视频生成 API...")
print("=" * 60)
print(f"封面图片：{cover_path}")
print(f"提示词：{prompt[:50]}...")
print(f"API 地址：{upload_url}")
print()

# 需要先获取登录状态
# 使用浏览器会话来获取 cookie
import http.cookiejar
import urllib.request

# 创建 CookieJar 来保存 cookie
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))

# 先访问主页获取 cookie
try:
    print("正在获取登录状态...")
    opener.open("https://aihuanying.com/", timeout=10)
    
    # 检查是否有登录 cookie
    logged_in = False
    for cookie in cookie_jar:
        if "token" in cookie.name or "session" in cookie.name or "auth" in cookie.name:
            print(f"找到认证 cookie: {cookie.name}")
            logged_in = True
    
    if not logged_in:
        print("未检测到登录状态，需要手动登录")
        print("请在浏览器中登录 aihuanying.com 后重试")
        sys.exit(1)
        
except Exception as e:
    print(f"获取登录状态失败：{e}")
    sys.exit(1)

# 准备文件上传
print("\n正在上传封面图片...")
with open(cover_path, 'rb') as f:
    files = {
        'file': ('cover.jpg', f, 'image/jpeg')
    }
    
    # 上传文件
    upload_resp = opener.open(
        urllib.request.Request(
            f"{base_url}/api/v1/files/upload",
            data=files,
            headers={}  # multipart/form-data 会自动设置
        ),
        timeout=30
    )
    
    upload_result = json.loads(upload_resp.read().decode('utf-8'))
    print(f"文件上传结果：{json.dumps(upload_result, ensure_ascii=False)}")
    
    # 获取文件 URL
    file_url = upload_result.get('data', {}).get('url') or upload_result.get('url')
    if not file_url:
        print("文件上传失败，未获取到 URL")
        sys.exit(1)
    
    print(f"文件 URL: {file_url}")

# 调用视频生成接口
print("\n正在提交视频生成任务...")
payload = {
    "prompt": prompt,
    "imageUrls": [file_url],  # 参考图 URL
    "ratio": "9:16",
    "duration": 10,
    "quality": "standard"
}

req = urllib.request.Request(
    upload_url,
    data=json.dumps(payload).encode('utf-8'),
    headers={
        "Content-Type": "application/json"
    },
    method="POST"
)

try:
    response = opener.open(req, timeout=180)
    result = json.loads(response.read().decode('utf-8'))
    
    print("=" * 60)
    print("视频生成结果:")
    print("=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("=" * 60)
    
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
            print(f"视频正在生成中，请稍后查询状态")
    else:
        print(f"\n✗ 视频生成失败：{result.get('message') or result.get('msg')}")
        
except urllib.error.HTTPError as he:
    err_body = he.read().decode('utf-8', errors='replace')
    print(f"HTTP 错误 {he.code}: {err_body}")
except Exception as e:
    print(f"发生错误：{e}")
