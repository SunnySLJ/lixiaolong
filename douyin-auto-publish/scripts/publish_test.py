#!/usr/bin/env python3
"""
发布测试视频
"""

import asyncio
import sys
import logging
import codecs

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

sys.path.insert(0, '.')
from publisher.douyin_publisher import DouyinPublisher

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def main():
    print("=" * 60)
    print("抖音发布工具 - 发布视频")
    print("=" * 60)
    print()
    
    # 视频信息
    video_path = "./storage/videos/test.mp4"
    title = "AI 自动化测试视频"
    description = "使用抖音发布工具自动上传 #AI #自动化 #科技前沿"
    
    print(f"视频：{video_path}")
    print(f"标题：{title}")
    print(f"描述：{description}")
    print()
    
    publisher = DouyinPublisher()
    
    # 检查登录
    print("检查登录状态...")
    if not await publisher.check_login("default"):
        print("未登录，请先运行登录脚本")
        return
    
    print("已登录，开始发布...")
    print()
    
    # 发布
    result = await publisher.publish(
        video_path=video_path,
        title=title,
        description=description,
        profile="default"
    )
    
    print()
    print("=" * 60)
    if result["success"]:
        print("发布成功！")
        if result.get("url"):
            print(f"视频链接：{result['url']}")
    else:
        print(f"发布失败：{result['message']}")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
