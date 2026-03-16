@echo off
chcp 65001 >nul
echo ============================================================
echo 抖音一键发布工具 - 安装测试
echo ============================================================
echo.

echo 1. 检查 Python 版本...
python --version
echo.

echo 2. 安装 Python 依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 依赖安装失败，请手动运行：pip install -r requirements.txt
    pause
    exit /b 1
)
echo.

echo 3. 安装 Playwright 浏览器...
playwright install chromium
if errorlevel 1 (
    echo 浏览器安装失败，请手动运行：playwright install chromium
    pause
    exit /b 1
)
echo.

echo 4. 创建存储目录...
if not exist storage\cookies mkdir storage\cookies
if not exist storage\videos mkdir storage\videos
echo 存储目录已创建
echo.

echo ============================================================
echo 安装完成！
echo ============================================================
echo.
echo 下一步:
echo.
echo 1. 登录抖音
echo    python scripts\login.py
echo.
echo 2. 发布视频
echo    python scripts\publish.py --video .\test.mp4 --title "我的视频"
echo.
echo 3. 查看帮助
echo    python scripts\publish.py --help
echo.
echo 详细文档:
echo - README.md - 项目说明
echo - QUICKSTART.md - 快速开始指南
echo.
echo 祝你使用愉快！
echo ============================================================
pause
