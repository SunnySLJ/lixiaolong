"""
抖音官方 OpenAPI 发布工具

参考：https://open.douyin.com/platform/resource/docs/ability/content-management/douyin-publish-solution/
参考项目：https://github.com/ddean2009/MoneyPrinterPlus

功能：
1. OAuth 2.0 用户授权
2. 视频上传
3. 视频发布
4. 视频管理（查询、删除）
5. 数据统计

使用前准备：
1. 企业资质证书
2. 在抖音开放平台创建应用
3. 获取 client_key 和 client_secret
4. 完成 OAuth 授权流程获取 access_token
"""

import requests
import json
import os
import hashlib
import time
from typing import Optional, Dict, Any
from pathlib import Path


class DouyinOpenAPI:
    """抖音开放平台 API 客户端"""
    
    def __init__(self, client_key: str, client_secret: str):
        """
        初始化 API 客户端
        
        Args:
            client_key: 应用的 client_key
            client_secret: 应用的 client_secret
        """
        self.client_key = client_key
        self.client_secret = client_secret
        self.access_token = None
        self.refresh_token = None
        self.token_expires_at = 0
        
        # API 端点
        self.base_url = "https://open.douyin.com"
        self.oauth_url = "https://open.douyin.com/oauth"
        
    # ==================== OAuth 授权 ====================
    
    def get_oauth_url(self, redirect_uri: str, scope: str = "user_info,video.create,video.upload") -> str:
        """
        获取 OAuth 授权 URL
        
        Args:
            redirect_uri: 授权回调地址
            scope: 授权范围
            
        Returns:
            OAuth 授权 URL
        """
        params = {
            "client_key": self.client_key,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "response_type": "code",
            "state": hashlib.md5(str(time.time()).encode()).hexdigest()
        }
        
        return f"{self.oauth_url}/authorize?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    
    def get_access_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """
        使用授权码获取 access_token
        
        Args:
            code: 授权码
            redirect_uri: 授权回调地址
            
        Returns:
            包含 access_token 的响应
        """
        url = f"{self.oauth_url}/access_token/"
        
        params = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
        
        response = requests.get(url, params=params)
        result = response.json()
        
        if result.get("error_code") == 0:
            data = result.get("data", {})
            self.access_token = data.get("access_token")
            self.refresh_token = data.get("refresh_token")
            self.token_expires_at = int(time.time()) + data.get("expires_in", 7200)
            
        return result
    
    def refresh_access_token(self) -> Dict[str, Any]:
        """
        刷新 access_token
        
        Returns:
            包含新 access_token 的响应
        """
        if not self.refresh_token:
            raise Exception("refresh_token 不存在，请重新授权")
        
        url = f"{self.oauth_url}/refresh_token/"
        
        params = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        
        response = requests.get(url, params=params)
        result = response.json()
        
        if result.get("error_code") == 0:
            data = result.get("data", {})
            self.access_token = data.get("access_token")
            self.refresh_token = data.get("refresh_token")
            self.token_expires_at = int(time.time()) + data.get("expires_in", 7200)
            
        return result
    
    def check_token_valid(self) -> bool:
        """检查 token 是否有效"""
        if not self.access_token:
            return False
        
        # 提前 5 分钟刷新
        if int(time.time()) > self.token_expires_at - 300:
            try:
                self.refresh_access_token()
            except:
                return False
        
        return True
    
    # ==================== 视频上传 ====================
    
    def upload_video(self, video_path: str, title: str = "") -> Dict[str, Any]:
        """
        上传视频到抖音
        
        Args:
            video_path: 视频文件路径
            title: 视频标题
            
        Returns:
            包含 video_id 的响应
        """
        if not self.check_token_valid():
            raise Exception("access_token 无效，请重新授权")
        
        url = f"{self.base_url}/api/douyin/v1/video/upload_video/"
        
        # 检查文件
        if not os.path.exists(video_path):
            raise Exception(f"视频文件不存在：{video_path}")
        
        # 准备文件
        files = {
            "video": (os.path.basename(video_path), open(video_path, "rb"), "video/mp4")
        }
        
        params = {
            "access_token": self.access_token,
            "title": title
        }
        
        response = requests.post(url, params=params, files=files)
        result = response.json()
        
        # 关闭文件
        files["video"][1].close()
        
        return result
    
    # ==================== 视频发布 ====================
    
    def create_video(self, 
                     video_id: str, 
                     text: str, 
                     poi_id: Optional[str] = None,
                     poi_name: Optional[str] = None,
                     micro_app_id: Optional[str] = None,
                     micro_app_title: Optional[str] = None,
                     micro_app_url: Optional[str] = None) -> Dict[str, Any]:
        """
        发布视频到抖音
        
        Args:
            video_id: 上传视频后获得的 video_id
            text: 视频标题和描述（可包含#话题 @用户）
            poi_id: 地理位置 ID（可选）
            poi_name: 地理位置名称（可选）
            micro_app_id: 小程序 ID（可选）
            micro_app_title: 小程序标题（可选）
            micro_app_url: 小程序参数（可选）
            
        Returns:
            发布结果
        """
        if not self.check_token_valid():
            raise Exception("access_token 无效，请重新授权")
        
        url = f"{self.base_url}/api/douyin/v1/video/create/"
        
        params = {
            "access_token": self.access_token
        }
        
        data = {
            "video_id": video_id,
            "text": text
        }
        
        # 可选参数
        if poi_id:
            data["poi_id"] = poi_id
        if poi_name:
            data["poi_name"] = poi_name
        if micro_app_id:
            data["micro_app_id"] = micro_app_id
        if micro_app_title:
            data["micro_app_title"] = micro_app_title
        if micro_app_url:
            data["micro_app_url"] = micro_app_url
        
        response = requests.post(url, params=params, json=data)
        return response.json()
    
    # ==================== 视频管理 ====================
    
    def list_videos(self, 
                    max_cursor: int = 0, 
                    count: int = 10) -> Dict[str, Any]:
        """
        获取已发布的视频列表
        
        Args:
            max_cursor: 分页游标
            count: 每页数量（最大 20）
            
        Returns:
            视频列表
        """
        if not self.check_token_valid():
            raise Exception("access_token 无效，请重新授权")
        
        url = f"{self.base_url}/api/douyin/v1/video/list/"
        
        params = {
            "access_token": self.access_token,
            "max_cursor": max_cursor,
            "count": min(count, 20)
        }
        
        response = requests.get(url, params=params)
        return response.json()
    
    def delete_video(self, video_id: str) -> Dict[str, Any]:
        """
        删除视频
        
        Args:
            video_id: 要删除的视频 ID
            
        Returns:
            删除结果
        """
        if not self.check_token_valid():
            raise Exception("access_token 无效，请重新授权")
        
        url = f"{self.base_url}/api/douyin/v1/video/delete/"
        
        params = {
            "access_token": self.access_token,
            "video_id": video_id
        }
        
        response = requests.post(url, params=params)
        return response.json()
    
    # ==================== 数据统计 ====================
    
    def get_video_data(self, video_id: str) -> Dict[str, Any]:
        """
        获取视频数据（播放量、点赞、评论等）
        
        Args:
            video_id: 视频 ID
            
        Returns:
            视频统计数据
        """
        if not self.check_token_valid():
            raise Exception("access_token 无效，请重新授权")
        
        url = f"{self.base_url}/api/douyin/v1/video/data/"
        
        params = {
            "access_token": self.access_token,
            "video_id": video_id
        }
        
        response = requests.get(url, params=params)
        return response.json()
    
    # ==================== 便捷方法 ====================
    
    def publish_video_file(self, 
                          video_path: str, 
                          title: str, 
                          description: str = "") -> Dict[str, Any]:
        """
        一键发布视频文件（上传 + 发布）
        
        Args:
            video_path: 视频文件路径
            title: 视频标题
            description: 视频描述（可包含#话题）
            
        Returns:
            发布结果
        """
        print(f"📹 正在上传视频：{video_path}")
        upload_result = self.upload_video(video_path, title)
        
        if upload_result.get("error_code") != 0:
            print(f"❌ 上传失败：{upload_result.get('description', '未知错误')}")
            return upload_result
        
        video_id = upload_result.get("data", {}).get("video_id")
        print(f"✅ 上传成功，video_id: {video_id}")
        
        # 组合标题和描述
        text = f"{title} {description}"
        
        print(f"📝 正在发布视频：{text}")
        publish_result = self.create_video(video_id, text)
        
        if publish_result.get("error_code") == 0:
            print(f"✅ 发布成功！")
        else:
            print(f"❌ 发布失败：{publish_result.get('description', '未知错误')}")
        
        return publish_result


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # 1. 初始化客户端
    client = DouyinOpenAPI(
        client_key="你的 client_key",
        client_secret="你的 client_secret"
    )
    
    # 2. 获取授权（需要用户手动操作）
    oauth_url = client.get_oauth_url("http://localhost:8000/callback")
    print(f"请在浏览器打开以下链接进行授权：\n{oauth_url}")
    
    # 3. 用户授权后，获取 code 并换取 token
    # code = input("请输入授权码：")
    # result = client.get_access_token(code, "http://localhost:8000/callback")
    
    # 4. 发布视频
    # result = client.publish_video_file(
    #     video_path="./video.mp4",
    #     title="视频标题",
    #     description="视频描述 #话题 #标签"
    # )
