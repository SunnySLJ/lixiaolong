@echo off
echo ============================================================
echo 启动 Chrome（带调试端口）
echo ============================================================
echo.
echo 这将会：
echo 1. 启动 Chrome 浏览器（带远程调试端口 9222）
echo 2. 打开抖音创作者页面
echo 3. 保持浏览器运行
echo.
echo 扫码登录后，运行 upload.bat 开始上传视频
echo.
pause

start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\爽爽\.openclaw\workspace\skills\douyin-video-upload\.chrome-profile" --no-first-run --no-default-browser-check https://creator.douyin.com/creator-micro/content/upload

echo.
echo Chrome 已启动！
echo 请在浏览器中完成抖音登录
echo.
echo 登录后，关闭此窗口前可以运行 upload.bat 上传视频
pause
