#!/usr/bin/env python3
"""
安装和测试脚本
验证项目是否可以正常运行
"""

import sys
import subprocess
import os

def print_header(text):
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")

def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"正在{description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print(f"✅ {description}成功")
            return True
        else:
            print(f"❌ {description}失败")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ {description}异常：{e}")
        return False

def main():
    print_header("抖音一键发布工具 - 安装测试")
    
    # 1. 检查 Python 版本
    print("1. 检查 Python 版本...")
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 9:
        print(f"✅ Python 版本：{python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"❌ Python 版本过低，需要 3.9+，当前：{python_version.major}.{python_version.minor}")
        return
    
    # 2. 安装依赖
    print_header("2. 安装 Python 依赖")
    if not run_command("pip install -r requirements.txt", "安装依赖"):
        print("\n⚠️ 依赖安装失败，请手动运行：pip install -r requirements.txt")
        return
    
    # 3. 安装 Playwright 浏览器
    print_header("3. 安装 Playwright 浏览器")
    if not run_command("playwright install chromium", "安装浏览器"):
        print("\n⚠️ 浏览器安装失败，请手动运行：playwright install chromium")
        return
    
    # 4. 创建存储目录
    print_header("4. 创建存储目录")
    os.makedirs("./storage/cookies", exist_ok=True)
    os.makedirs("./storage/videos", exist_ok=True)
    print("✅ 存储目录已创建")
    
    # 5. 测试导入
    print_header("5. 测试模块导入")
    try:
        from publisher.douyin_publisher import DouyinPublisher
        print("✅ 模块导入成功")
    except Exception as e:
        print(f"❌ 模块导入失败：{e}")
        return
    
    # 6. 显示使用说明
    print_header("✅ 安装完成！")
    
    print("""
🎉 恭喜！抖音一键发布工具已安装成功！

下一步:

1. 登录抖音
   python scripts/login.py

2. 发布视频
   python scripts/publish.py --video ./test.mp4 --title "我的视频" --desc "#话题"

3. 查看帮助
   python scripts/publish.py --help

详细文档:
- README.md - 项目说明
- QUICKSTART.md - 快速开始指南

祝你使用愉快！🎉
    """)
    
    print_header("安装测试完成")

if __name__ == "__main__":
    main()
