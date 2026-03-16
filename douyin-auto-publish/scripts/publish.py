#!/usr/bin/env python3
"""
抖音发布脚本
一键发布视频到抖音
"""

import asyncio
import sys
import argparse
import logging
from pathlib import Path
import codecs

# 设置控制台编码
if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 添加项目根目录到路径
sys.path.insert(0, '.')

from publisher.douyin_publisher import DouyinPublisher

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='抖音一键发布工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本发布
  python scripts/publish.py --video ./test.mp4 --title "我的视频"
  
  # 带描述发布
  python scripts/publish.py --video ./test.mp4 --title "我的视频" --desc "今天的好心情 #日常"
  
  # 指定配置
  python scripts/publish.py --video ./test.mp4 --title "我的视频" --profile myaccount
  
  # 私密发布
  python scripts/publish.py --video ./test.mp4 --title "我的视频" --privacy private
        """
    )
    
    parser.add_argument(
        '--video', '-v',
        required=True,
        help='视频文件路径（MP4 格式）'
    )
    
    parser.add_argument(
        '--title', '-t',
        required=True,
        help='视频标题'
    )
    
    parser.add_argument(
        '--desc', '-d',
        default='',
        help='视频描述（可包含话题标签）'
    )
    
    parser.add_argument(
        '--cover', '-c',
        default='',
        help='封面图片路径（可选）'
    )
    
    parser.add_argument(
        '--privacy', '-p',
        choices=['public', 'friend', 'private'],
        default='public',
        help='隐私设置：public=公开，friend=好友可见，private=私密（默认：public）'
    )
    
    parser.add_argument(
        '--profile',
        default='default',
        help='使用的配置名称（默认：default）'
    )
    
    parser.add_argument(
        '--check-login',
        action='store_true',
        help='只检查登录状态，不发布'
    )
    
    return parser.parse_args()


async def main():
    """主函数"""
    args = parse_args()
    
    print("=" * 60)
    print("抖音一键发布工具")
    print("=" * 60)
    print()
    
    # 检查视频文件
    video_path = Path(args.video)
    if not video_path.exists():
        print(f"❌ 视频文件不存在：{video_path}")
        return
    
    print(f"📹 视频：{video_path.name}")
    print(f"📝 标题：{args.title}")
    print(f"📄 描述：{args.desc or '无'}")
    print(f"🔒 隐私：{args.privacy}")
    print(f"👤 配置：{args.profile}")
    print()
    
    # 创建发布器
    publisher = DouyinPublisher()
    
    # 检查登录状态
    if args.check_login:
        print("🔍 检查登录状态...")
        if await publisher.check_login(args.profile):
            print("✅ 已登录")
        else:
            print("❌ 未登录")
            print("\n请先运行：python scripts/login.py")
        return
    
    # 检查是否已登录
    if not await publisher.check_login(args.profile):
        print("❌ 未登录")
        print("\n请先运行：python scripts/login.py")
        return
    
    print("✅ 登录状态正常")
    print()
    
    # 确认发布
    confirm = input("确认发布？(y/n): ").strip().lower()
    if confirm != 'y':
        print("已取消发布")
        return
    
    # 执行发布
    print("\n🚀 开始发布...")
    result = await publisher.publish(
        video_path=str(video_path),
        title=args.title,
        description=args.desc,
        cover_path=args.cover if args.cover else None,
        privacy=args.privacy,
        profile=args.profile
    )
    
    print()
    print("=" * 60)
    if result["success"]:
        print("✅ 发布成功！")
        if result.get("url"):
            print(f"🔗 视频链接：{result['url']}")
    else:
        print(f"❌ 发布失败：{result['message']}")
        print("\n可能的原因：")
        print("  1. Cookie 已过期，请重新登录：python scripts/login.py")
        print("  2. 视频格式不支持，请使用 MP4 格式")
        print("  3. 网络问题，请检查网络连接")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
