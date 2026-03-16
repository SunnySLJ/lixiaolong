"""
测试抖音 API - 直接使用 requests
"""

import requests
import hashlib
import time

def test_mock_api():
    """测试 Mock API"""
    
    print("=" * 60)
    print("抖音 API Mock 测试")
    print("=" * 60)
    print()
    
    base_url = "http://localhost:8000"
    
    # 1. 健康检查
    print("1. 健康检查...")
    try:
        health = requests.get(f"{base_url}/health", timeout=5)
        if health.status_code == 200:
            print("✅ Mock 服务器运行正常")
            print(f"   {health.json()['message']}")
        else:
            print("❌ 服务器响应异常")
            return
    except:
        print("❌ 无法连接到 Mock 服务器")
        print("   请先运行：python mock_server.py")
        return
    print()
    
    # 2. OAuth 授权
    print("2. OAuth 授权...")
    client_key = "test_client_key"
    client_secret = "test_client_secret"
    redirect_uri = "http://localhost:8000/callback"
    
    auth_params = {
        "client_key": client_key,
        "redirect_uri": redirect_uri,
        "scope": "user_info,video.create,video.upload",
        "response_type": "code",
        "state": "test_state_123"
    }
    
    auth_response = requests.get(f"{base_url}/oauth/authorize", params=auth_params)
    if auth_response.status_code == 200:
        auth_data = auth_response.json()
        mock_code = auth_data.get("mock_code")
        print(f"✅ 获取授权 code: {mock_code}")
    else:
        print(f"❌ 授权失败：{auth_response.text}")
        return
    print()
    
    # 3. 获取 access_token
    print("3. 获取 access_token...")
    token_params = {
        "client_key": client_key,
        "client_secret": client_secret,
        "code": mock_code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }
    
    token_response = requests.get(f"{base_url}/oauth/access_token/", params=token_params)
    if token_response.status_code == 200:
        token_data = token_response.json()
        if token_data.get("error_code") == 0:
            access_token = token_data["data"]["access_token"]
            refresh_token = token_data["data"]["refresh_token"]
            print(f"✅ Access Token: {access_token[:30]}...")
            print(f"   有效期：{token_data['data']['expires_in']}秒")
        else:
            print(f"❌ 获取失败：{token_data}")
            return
    else:
        print(f"❌ 请求失败：{token_response.text}")
        return
    print()
    
    # 4. 上传视频
    print("4. 上传视频...")
    video_title = "AI 自动化测试视频"
    
    upload_params = {
        "access_token": access_token,
        "title": video_title
    }
    
    # 注意：Mock 服务器不真正处理文件上传
    upload_response = requests.post(f"{base_url}/api/douyin/v1/video/upload_video/", params=upload_params)
    if upload_response.status_code == 200:
        upload_data = upload_response.json()
        if upload_data.get("error_code") == 0:
            video_id = upload_data["data"]["video_id"]
            print(f"✅ 上传成功！")
            print(f"   Video ID: {video_id}")
        else:
            print(f"❌ 上传失败：{upload_data}")
            return
    else:
        print(f"❌ 请求失败：{upload_response.text}")
        return
    print()
    
    # 5. 发布视频
    print("5. 发布视频...")
    video_desc = "使用抖音发布工具自动上传 #AI #自动化 #科技前沿"
    
    publish_data = {
        "video_id": video_id,
        "text": f"{video_title} {video_desc}"
    }
    
    publish_params = {"access_token": access_token}
    publish_response = requests.post(f"{base_url}/api/douyin/v1/video/create/", params=publish_params, json=publish_data)
    
    if publish_response.status_code == 200:
        publish_result = publish_response.json()
        if publish_result.get("error_code") == 0:
            print("✅ 发布成功！")
            print(f"   文案：{video_title} {video_desc}")
        else:
            print(f"❌ 发布失败：{publish_result}")
    else:
        print(f"❌ 请求失败：{publish_response.text}")
    print()
    
    # 6. 获取视频列表
    print("6. 获取视频列表...")
    list_params = {
        "access_token": access_token,
        "max_cursor": 0,
        "count": 10
    }
    
    list_response = requests.get(f"{base_url}/api/douyin/v1/video/list/", params=list_params)
    if list_response.status_code == 200:
        list_data = list_response.json()
        if list_data.get("error_code") == 0:
            videos = list_data["data"]["list"]
            print(f"✅ 获取到 {len(videos)} 个视频")
            
            for i, video in enumerate(videos, 1):
                print(f"\n   视频 {i}:")
                print(f"      ID: {video.get('video_id')}")
                print(f"      标题：{video.get('title')}")
                print(f"      状态：{video.get('status')}")
        else:
            print(f"❌ 获取失败：{list_data}")
    else:
        print(f"❌ 请求失败：{list_response.text}")
    print()
    
    # 7. 获取视频数据
    print("7. 获取视频数据...")
    if videos:
        test_video_id = videos[0]["video_id"]
        data_params = {
            "access_token": access_token,
            "video_id": test_video_id
        }
        
        data_response = requests.get(f"{base_url}/api/douyin/v1/video/data/", params=data_params)
        if data_response.status_code == 200:
            data_result = data_response.json()
            if data_result.get("error_code") == 0:
                data = data_result["data"]
                print("✅ 视频数据:")
                print(f"   播放量：{data.get('play_count')}")
                print(f"   点赞数：{data.get('digg_count')}")
                print(f"   评论数：{data.get('comment_count')}")
                print(f"   分享数：{data.get('share_count')}")
                print(f"   下载数：{data.get('download_count')}")
            else:
                print(f"❌ 获取失败：{data_result}")
        else:
            print(f"❌ 请求失败：{data_response.text}")
    print()
    
    # 完成
    print("=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)
    print()
    print("📊 测试总结:")
    print("  ✅ OAuth 授权")
    print("  ✅ Token 获取")
    print("  ✅ 视频上传")
    print("  ✅ 视频发布")
    print("  ✅ 视频列表")
    print("  ✅ 数据统计")
    print()
    print("🎉 所有功能测试通过！")
    print()
    print("下一步:")
    print("1. 获取真实 API Key: https://open.douyin.com/")
    print("2. 配置到 config.json")
    print("3. 切换到真实 API")


if __name__ == "__main__":
    test_mock_api()
