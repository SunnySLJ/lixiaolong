#!/usr/bin/env python3
"""
抖音登录脚本
扫码登录并保存 Cookie
"""

import asyncio
import sys
import logging

# 添加项目根目录到路径
sys.path.insert(0, '.')

from publisher.douyin_publisher import DouyinPublisher

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """主函数"""
    print("=" * 60)
    print("抖音一键发布工具 - 登录")
    print("=" * 60)
    print()
    
    # 获取配置名称
    profile = input("请输入配置名称（默认：default）：").strip() or "default"
    
    print(f"\n使用配置：{profile}")
    print()
    
    # 创建发布器
    publisher = DouyinPublisher()
    
    # 检查是否已登录
    if await publisher.check_login(profile):
        print(f"⚠️ 配置 {profile} 已登录")
        choice = input("是否重新登录？(y/n): ").strip().lower()
        if choice != 'y':
            print("已取消登录")
            return
        # 退出登录
        await publisher.logout(profile)
    
    print("\n即将打开浏览器，请使用抖音 APP 扫码登录")
    print("提示：登录成功后会自动保存 Cookie，下次无需重复登录")
    print()
    
    # 执行登录
    success = await publisher.login(profile)
    
    print()
    print("=" * 60)
    if success:
        print("✅ 登录成功！")
        print(f"Cookie 已保存至：./storage/cookies/{profile}.json")
        print()
        print("现在可以使用 publish.py 发布视频了")
        print("示例：python scripts/publish.py --video ./test.mp4 --title \"我的视频\"")
    else:
        print("❌ 登录失败")
        print("请检查网络连接后重试")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
