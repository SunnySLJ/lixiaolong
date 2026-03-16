@echo off
chcp 65001 >nul
echo ============================================================
echo 抖音发布工具 - 登录
echo ============================================================
echo.
echo 即将打开浏览器，请使用抖音 APP 扫码登录
echo.
echo 提示：
echo 1. 打开抖音 APP
echo 2. 点击右上角扫描图标
echo 3. 扫描屏幕上的二维码
echo 4. 确认登录
echo.
echo 登录成功后浏览器会自动关闭
echo ============================================================
echo.

python scripts\quick_login.py

echo.
echo ============================================================
if %errorlevel% equ 0 (
    echo 登录完成！
    echo.
    echo 下一步：发布视频
    echo 运行：python scripts\publish.py --video ./storage/videos/test.mp4 --title "我的视频" --desc "#AI #自动化"
) else (
    echo 登录失败，请重试
)
echo ============================================================
pause
