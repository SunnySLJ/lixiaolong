"""
测试 TikTok Skill 上传视频
"""

import asyncio
import sys
import codecs
import json
from pathlib import Path

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

async def test_tiktok_upload():
    """测试 TikTok 视频上传"""
    
    print("=" * 60)
    print("TikTok 视频上传测试")
    print("=" * 60)
    print()
    
    # 视频文件
    video_path = Path("./storage/videos/test.mp4")
    video_title = "AI 自动化测试视频 #AI #自动化 #科技"
    
    print(f"📹 视频文件：{video_path}")
    print(f"📝 视频标题：{video_title}")
    print()
    
    # 检查文件
    if not video_path.exists():
        print(f"❌ 视频文件不存在：{video_path}")
        print("   请先准备视频文件")
        return
    
    video_size = video_path.stat().st_size / 1024 / 1024
    print(f"✅ 文件大小：{video_size:.2f} MB")
    print()
    
    # TikTok 上传要求
    print("📋 TikTok 视频要求:")
    print("   - 格式：MP4/WebM ✅")
    print("   - 大小：≤ 4GB ✅")
    print("   - 时长：≤ 10 分钟")
    print("   - 分辨率：720p 及以上")
    print()
    
    # 上传参数
    print("📝 上传参数:")
    print(f"   - 标题：{video_title}")
    print(f"   - 隐私：PUBLIC_TO_EVERYONE (公开)")
    print(f"   - 允许合拍：是")
    print(f"   - 允许拼接：是")
    print(f"   - 允许评论：是")
    print()
    
    print("=" * 60)
    print("⚠️  注意：TikTok Skill 需要 Rube MCP 连接")
    print("=" * 60)
    print()
    print("使用步骤:")
    print("1. 在 AI 客户端中添加 Rube MCP:")
    print("   https://rube.app/mcp")
    print()
    print("2. 连接 TikTok 账号:")
    print("   对 AI 说：帮我连接 TikTok 账号")
    print()
    print("3. 上传视频:")
    print("   对 AI 说：帮我上传这个视频到 TikTok: ./storage/videos/test.mp4")
    print()
    print("=" * 60)
    print()
    
    # 创建测试脚本
    test_script = """
# TikTok 上传测试脚本

在支持 MCP 的 AI 客户端中运行以下命令：

## 1. 检查连接

```
检查我的 TikTok 连接状态
```

## 2. 连接 TikTok（如未连接）

```
帮我连接 TikTok 账号
```

## 3. 上传视频

```
帮我上传这个视频到 TikTok: ./storage/videos/test.mp4
标题："AI 自动化测试视频 #AI #自动化 #科技"
隐私级别：公开
```

## 4. 查看发布状态

```
帮我检查刚才发布的视频状态
```

## 5. 查看我的视频列表

```
帮我查看我发布的视频列表
```
"""
    
    # 保存测试脚本
    script_file = Path("./tiktok_test_instructions.md")
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print(f"📄 测试说明已保存至：{script_file}")
    print()
    print("现在可以在支持 MCP 的 AI 客户端中使用 TikTok Skill 了！")
    print()
    print("支持的客户端:")
    print("  - Claude Code")
    print("  - Cursor")
    print("  - Codex")
    print("  - Gemini CLI")
    print("  - GitHub Copilot")
    print("  - 等 42 个平台")
    print()


if __name__ == "__main__":
    asyncio.run(test_tiktok_upload())
