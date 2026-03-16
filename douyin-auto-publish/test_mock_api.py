"""
测试抖音 API（使用 Mock 服务器）

无需真实 API Key，可以测试完整的 OAuth 和发布流程
"""

from douyin_openapi import DouyinOpenAPI
import sys

# Mock 服务器地址
MOCK_BASE_URL = "http://localhost:8000"

def test_mock_api():
    """测试 Mock API"""
    
    print("=" * 60)
    print("抖音 API Mock 测试")
    print("=" * 60)
    print()
    
    # 1. 初始化客户端（使用 Mock 凭证）
    print("1. 初始化客户端...")
    client = DouyinOpenAPI(
        client_key="test_client_key",
        client_secret="test_client_secret"
    )
    print("✅ 客户端初始化成功")
    print()
    
    # 2. 获取 OAuth 授权 URL
    print("2. 获取 OAuth 授权 URL...")
    oauth_url = client.get_oauth_url("http://localhost:8000/callback")
    print(f"   OAuth URL: {oauth_url[:100]}...")
    print("✅ OAuth URL 生成成功")
    print()
    
    # 3. 模拟授权（实际使用时需要用户扫码）
    print("3. 模拟授权获取 code...")
    # Mock code
    mock_code = "test_auth_code_123456"
    print(f"   Code: {mock_code}")
    print()
    
    # 4. 获取 access_token
    print("4. 获取 access_token...")
    result = client.get_access_token(mock_code, "http://localhost:8000/callback")
    
    if result.get("error_code") == 0:
        print(f"✅ Access Token: {client.access_token[:20]}...")
        print(f"   Expires In: {result.get('data', {}).get('expires_in')}s")
    else:
        print(f"❌ 获取失败：{result}")
        return
    print()
    
    # 5. 上传视频（模拟）
    print("5. 上传视频（模拟）...")
    # 注意：Mock 服务器不会真正上传文件
    # 这里只是测试接口调用
    try:
        upload_result = client.upload_video("./test_video.mp4", "测试视频")
        if upload_result.get("error_code") == 0:
            video_id = upload_result.get("data", {}).get("video_id")
            print(f"✅ 上传成功，video_id: {video_id}")
        else:
            print(f"❌ 上传失败：{upload_result}")
            return
    except FileNotFoundError:
        print("⚠️  测试文件不存在，跳过实际上传")
        # 使用 Mock video_id
        video_id = "video_mock_123"
        print(f"   使用 Mock video_id: {video_id}")
    print()
    
    # 6. 发布视频
    print("6. 发布视频...")
    publish_result = client.create_video(
        video_id=video_id,
        text="测试视频 #AI #自动化",
        poi_id=None
    )
    
    if publish_result.get("error_code") == 0:
        print("✅ 发布成功！")
    else:
        print(f"❌ 发布失败：{publish_result}")
    print()
    
    # 7. 获取视频列表
    print("7. 获取视频列表...")
    list_result = client.list_videos(count=10)
    
    if list_result.get("error_code") == 0:
        videos = list_result.get("data", {}).get("list", [])
        print(f"✅ 获取到 {len(videos)} 个视频")
        for video in videos:
            print(f"   - {video.get('title')} ({video.get('video_id')})")
    else:
        print(f"❌ 获取失败：{list_result}")
    print()
    
    # 8. 获取视频数据
    print("8. 获取视频数据（模拟）...")
    if videos:
        video_id = videos[0].get("video_id")
        data_result = client.get_video_data(video_id)
        
        if data_result.get("error_code") == 0:
            data = data_result.get("data", {})
            print("✅ 视频数据:")
            print(f"   播放量：{data.get('play_count')}")
            print(f"   点赞数：{data.get('digg_count')}")
            print(f"   评论数：{data.get('comment_count')}")
        else:
            print(f"❌ 获取失败：{data_result}")
    print()
    
    print("=" * 60)
    print("✅ Mock 测试完成！")
    print("=" * 60)
    print()
    print("下一步:")
    print("1. 启动 Mock 服务器：python mock_server.py")
    print("2. 访问 API 文档：http://localhost:8000/docs")
    print("3. 运行测试：python test_mock_api.py")
    print()
    print("提示:")
    print("- Mock 服务器用于测试代码逻辑")
    print("- 真实发布需要使用官方 API Key")
    print("- 官方 Key 申请：https://open.douyin.com/")


if __name__ == "__main__":
    test_mock_api()
