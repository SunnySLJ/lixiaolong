@echo off
echo ============================================================
echo 抖音视频上传（使用已登录的 Chrome）
echo ============================================================
echo.

set VIDEO_PATH=%~1
if "%VIDEO_PATH%"=="" set VIDEO_PATH=C:\Users\爽爽\Desktop\图片\2.mp4

echo 视频：%VIDEO_PATH%
echo.

python scripts\douyin_upload.py --video "%VIDEO_PATH%" --publish --use-existing-chrome --debug-port 9222

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ 上传完成！浏览器保持打开，你可以查看上传结果
) else (
    echo ❌ 上传失败，请检查 debug_error.png
)
pause
