#!/usr/bin/env python3
"""
抖音发布脚本 - 自动确认版
"""

import asyncio
import sys
import codecs
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

sys.path.insert(0, '.')
from publisher.douyin_publisher import DouyinPublisher

async def main():
    """主函数"""
    print("=" * 60)
    print("抖音发布工具 - 自动测试")
    print("=" * 60)
    print()
    
    # 视频信息
    video_path = Path("./storage/videos/test.mp4")
    title = "AI 自动化测试视频"
    description = "使用抖音发布工具自动上传 #AI #自动化 #科技前沿"
    
    print(f"📹 视频：{video_path.name}")
    print(f"📝 标题：{title}")
    print(f"📄 描述：{description}")
    print()
    
    # 检查文件
    if not video_path.exists():
        print(f"❌ 视频文件不存在：{video_path}")
        return
    
    # 创建发布器
    publisher = DouyinPublisher()
    
    # 检查登录
    print("🔍 检查登录状态...")
    if not await publisher.check_login("default"):
        print("❌ 未登录")
        print("\n请先运行：python scripts/quick_login.py")
        return
    
    print("✅ 登录状态正常")
    print()
    
    # 发布
    print("🚀 开始发布...")
    result = await publisher.publish(
        video_path=str(video_path),
        title=title,
        description=description,
        profile="default"
    )
    
    print()
    print("=" * 60)
    if result["success"]:
        print("🎉 发布成功！")
        if result.get("url"):
            print(f"🔗 视频链接：{result['url']}")
    else:
        print(f"❌ 发布失败：{result['message']}")
        print("\n可能的原因:")
        print("  1. Cookie 已过期，请重新登录：python scripts/quick_login.py")
        print("  2. 视频格式不支持，请使用 MP4 格式")
        print("  3. 网络问题，请检查网络连接")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
