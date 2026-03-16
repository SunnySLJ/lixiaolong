#!/usr/bin/env python3
"""
简化的抖音登录脚本 - 自动模式
"""

import asyncio
import sys
import logging
import codecs

# 设置控制台编码
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
    print("抖音登录 - 自动化模式")
    print("=" * 60)
    print()
    
    publisher = DouyinPublisher()
    
    print("即将打开浏览器...")
    print("请使用抖音 APP 扫描二维码登录")
    print("登录成功后会自动关闭浏览器并保存 Cookie")
    print()
    
    success = await publisher.login("default")
    
    print()
    print("=" * 60)
    if success:
        print("登录成功！Cookie 已保存")
        print()
        print("下一步：发布视频")
        print("命令：python scripts/publish.py -v ./video.mp4 -t \"标题\" -d \"描述\"")
    else:
        print("登录失败或超时")
        print("请检查网络连接后重试")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
