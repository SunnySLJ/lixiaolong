@echo off
chcp 65001 >nul
echo ============================================================
echo 抖音发布工具 - 快速测试
echo ============================================================
echo.
echo 这个脚本会帮你完成登录和发布测试
echo.
echo 步骤:
echo 1. 打开浏览器扫码登录
echo 2. 发布测试视频
echo.
echo ============================================================
echo.

echo 第 1 步：登录抖音
echo.
python scripts\quick_login.py
if errorlevel 1 (
    echo 登录失败，请检查网络连接
    pause
    exit /b 1
)

echo.
echo ============================================================
echo.
echo 第 2 步：发布视频
echo.
echo 请确保有以下文件:
echo   storage\videos\test.mp4
echo.
echo 然后运行发布命令:
echo   python scripts\publish.py --video ./storage/videos/test.mp4 --title "我的测试视频" --desc "AI 自动化测试 #AI #自动化"
echo.
echo ============================================================
pause
