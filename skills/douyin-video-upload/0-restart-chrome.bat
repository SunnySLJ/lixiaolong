@echo off
echo ============================================================
echo 重启 Chrome（带调试端口，保留你的账号数据）
echo ============================================================
echo.
echo 这会：
echo 1. 关闭所有 Chrome 窗口
echo 2. 等待 2 秒
echo 3. 用调试模式重新启动 Chrome（使用你的原有账号数据）
echo 4. 自动打开抖音创作者页面
echo.
echo 启动后，在浏览器中登录抖音，然后运行 1-upload.bat
echo.
pause

echo [1/3] 正在关闭所有 Chrome...
taskkill /F /IM chrome.exe
timeout /t 2 /nobreak >nul

echo [2/3] 启动 Chrome（调试模式）...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\爽爽\AppData\Local\Google\Chrome\User Data" --no-first-run https://creator.douyin.com/creator-micro/content/upload

echo [3/3] Chrome 已启动！
echo.
echo ============================================================
echo 下一步：
echo 1. 在打开的 Chrome 中登录抖音（如果还没登录）
echo 2. 登录后，运行 1-upload.bat 开始上传视频
echo ============================================================
echo.
pause
