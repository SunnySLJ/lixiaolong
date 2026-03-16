"""
抖音 API Mock 测试服务器

用于在没有真实 API Key 的情况下测试代码逻辑
模拟抖音开放平台的 OAuth 和视频发布接口
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import json
import hashlib
import time
import random

app = FastAPI(title="抖音 API Mock Server")

# Mock 数据
mock_db = {
    "videos": [],
    "tokens": {},
    "users": []
}

# ==================== 数据模型 ====================

class OAuthRequest(BaseModel):
    client_key: str
    client_secret: str
    code: str
    grant_type: str
    redirect_uri: str

class VideoUploadRequest(BaseModel):
    title: str

class VideoCreateRequest(BaseModel):
    video_id: str
    text: str
    poi_id: Optional[str] = None
    poi_name: Optional[str] = None

# ==================== OAuth 接口 ====================

@app.get("/oauth/authorize")
async def oauth_authorize(
    client_key: str,
    redirect_uri: str,
    scope: str,
    response_type: str,
    state: str
):
    """
    OAuth 授权页面（模拟）
    
    实际使用时会显示二维码让用户扫码授权
    """
    # 模拟授权成功，重定向回回调地址
    mock_code = hashlib.md5(f"{client_key}{time.time()}".encode()).hexdigest()[:32]
    
    redirect_url = f"{redirect_uri}?code={mock_code}&state={state}"
    
    return {
        "message": "请在浏览器中打开以下链接完成授权",
        "authorize_url": redirect_url,
        "mock_code": mock_code
    }

@app.get("/oauth/access_token/")
async def oauth_access_token(
    client_key: str,
    client_secret: str,
    code: str,
    grant_type: str,
    redirect_uri: str
):
    """
    获取 access_token（模拟）
    """
    # 验证 client_key 和 client_secret
    if client_key != "test_client_key" or client_secret != "test_client_secret":
        raise HTTPException(status_code=400, detail="Invalid client credentials")
    
    # 生成 token
    access_token = hashlib.md5(f"{code}{time.time()}".encode()).hexdigest()
    refresh_token = hashlib.md5(f"{access_token}refresh".encode()).hexdigest()
    
    # 保存 token
    mock_db["tokens"][access_token] = {
        "expires_at": int(time.time()) + 7200,
        "refresh_token": refresh_token,
        "client_key": client_key
    }
    
    return {
        "error_code": 0,
        "description": "Success",
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 7200,
            "scope": "user_info,video.create,video.upload"
        }
    }

@app.get("/oauth/refresh_token/")
async def oauth_refresh_token(
    client_key: str,
    client_secret: str,
    grant_type: str,
    refresh_token: str
):
    """
    刷新 access_token（模拟）
    """
    # 查找 refresh_token
    for token, data in mock_db["tokens"].items():
        if data["refresh_token"] == refresh_token:
            # 生成新 token
            new_access_token = hashlib.md5(f"{refresh_token}{time.time()}".encode()).hexdigest()
            
            mock_db["tokens"][new_access_token] = {
                "expires_at": int(time.time()) + 7200,
                "refresh_token": refresh_token,
                "client_key": client_key
            }
            
            return {
                "error_code": 0,
                "description": "Success",
                "data": {
                    "access_token": new_access_token,
                    "refresh_token": refresh_token,
                    "expires_in": 7200
                }
            }
    
    raise HTTPException(status_code=400, detail="Invalid refresh token")

# ==================== 视频上传接口 ====================

@app.post("/api/douyin/v1/video/upload_video/")
async def video_upload(
    access_token: str,
    title: str = ""
):
    """
    上传视频（模拟）
    
    实际接口需要 multipart/form-data 上传文件
    """
    # 验证 token
    if access_token not in mock_db["tokens"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # 生成 video_id
    video_id = f"video_{int(time.time())}_{random.randint(1000, 9999)}"
    
    # 保存视频信息
    mock_db["videos"].append({
        "video_id": video_id,
        "title": title,
        "create_time": int(time.time()),
        "status": "uploaded"
    })
    
    return {
        "error_code": 0,
        "description": "Success",
        "data": {
            "video_id": video_id,
            "title": title,
            "upload_time": int(time.time())
        }
    }

# ==================== 视频发布接口 ====================

@app.post("/api/douyin/v1/video/create/")
async def video_create(
    access_token: str,
    request: VideoCreateRequest
):
    """
    发布视频（模拟）
    """
    # 验证 token
    if access_token not in mock_db["tokens"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # 查找视频
    video = None
    for v in mock_db["videos"]:
        if v["video_id"] == request.video_id:
            video = v
            break
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # 更新视频状态
    video["status"] = "published"
    video["text"] = request.text
    video["poi_id"] = request.poi_id
    video["poi_name"] = request.poi_name
    video["publish_time"] = int(time.time())
    
    return {
        "error_code": 0,
        "description": "Success",
        "data": {
            "video_id": request.video_id,
            "text": request.text,
            "publish_time": int(time.time())
        }
    }

# ==================== 视频管理接口 ====================

@app.get("/api/douyin/v1/video/list/")
async def video_list(
    access_token: str,
    max_cursor: int = 0,
    count: int = 10
):
    """
    获取视频列表（模拟）
    """
    # 验证 token
    if access_token not in mock_db["tokens"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # 分页
    start = max_cursor
    end = max_cursor + min(count, 20)
    
    videos = mock_db["videos"][start:end]
    
    return {
        "error_code": 0,
        "description": "Success",
        "data": {
            "list": videos,
            "has_more": end < len(mock_db["videos"]),
            "max_cursor": end
        }
    }

@app.post("/api/douyin/v1/video/delete/")
async def video_delete(
    access_token: str,
    video_id: str
):
    """
    删除视频（模拟）
    """
    # 验证 token
    if access_token not in mock_db["tokens"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # 查找并删除视频
    for i, video in enumerate(mock_db["videos"]):
        if video["video_id"] == video_id:
            mock_db["videos"].pop(i)
            return {
                "error_code": 0,
                "description": "Success",
                "data": {
                    "video_id": video_id
                }
            }
    
    raise HTTPException(status_code=404, detail="Video not found")

@app.get("/api/douyin/v1/video/data/")
async def video_data(
    access_token: str,
    video_id: str
):
    """
    获取视频数据（模拟）
    """
    # 验证 token
    if access_token not in mock_db["tokens"]:
        raise HTTPException(status_code=401, detail="Invalid access token")
    
    # 查找视频
    video = None
    for v in mock_db["videos"]:
        if v["video_id"] == video_id:
            video = v
            break
    
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # 返回模拟数据
    return {
        "error_code": 0,
        "description": "Success",
        "data": {
            "video_id": video_id,
            "play_count": random.randint(100, 10000),
            "digg_count": random.randint(10, 1000),
            "comment_count": random.randint(0, 100),
            "share_count": random.randint(0, 50),
            "download_count": random.randint(0, 20)
        }
    }

# ==================== 健康检查 ====================

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "ok",
        "message": "Mock server is running",
        "test_credentials": {
            "client_key": "test_client_key",
            "client_secret": "test_client_secret"
        }
    }

# ==================== 启动服务器 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("抖音 API Mock 测试服务器")
    print("=" * 60)
    print()
    print("测试凭证:")
    print("  client_key: test_client_key")
    print("  client_secret: test_client_secret")
    print()
    print("API 文档:")
    print("  http://localhost:8000/docs")
    print()
    print("健康检查:")
    print("  http://localhost:8000/health")
    print()
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
