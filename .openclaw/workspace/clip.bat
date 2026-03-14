@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: Video Clip Tool - 视频剪辑工具
:: Usage: clip.bat <input> [options]

set INPUT=%~1
if "%INPUT%"=="" (
    echo 用法: clip.bat ^<输入视频^> [选项]
    echo.
    echo 选项:
    echo   --start TIME     开始时间 (如: 00:00:10 或 10)
    echo   --duration SEC   持续时间 (秒)
    echo   --end TIME       结束时间
    echo   --output FILE    输出文件名
    echo   --speed RATE     速度 (0.5=慢放, 2=快放)
    echo   --resolution WxH 分辨率 (如: 1280x720)
    echo   --format FMT     输出格式 (mp4, mov, gif)
    echo   --mute           静音输出
    echo.
    echo 示例:
    echo   clip.bat input.mp4 --start 10 --duration 5 --output cut.mp4
    echo   clip.bat input.mp4 --start 00:01:00 --end 00:02:00 --speed 2
    exit /b 1
)

set START_TIME=
set DURATION=
set END_TIME=
set OUTPUT=
set SPEED=
set RESOLUTION=
set FORMAT=mp4
set MUTE=

:: Parse arguments
shift
:parse_args
if "%~1"=="" goto :done_parse
if /i "%~1"=="--start" set START_TIME=%~2& shift& shift& goto :parse_args
if /i "%~1"=="--duration" set DURATION=%~2& shift& shift& goto :parse_args
if /i "%~1"=="--end" set END_TIME=%~2& shift& shift& goto :parse_args
if /i "%~1"=="--output" set OUTPUT=%~2& shift& shift& goto :parse_args
if /i "%~1"=="--speed" set SPEED=%~2& shift& shift& goto :parse_args
if /i "%~1"=="--resolution" set RESOLUTION=%~2& shift& shift& goto :parse_args
if /i "%~1"=="--format" set FORMAT=%~2& shift& shift& goto :parse_args
if /i "%~1"=="--mute" set MUTE=1& shift& goto :parse_args
shift
goto :parse_args
:done_parse

:: Default output name
if "%OUTPUT%"=="" (
    for %%F in ("%INPUT%") do set "BASENAME=%%~nF"
    set "OUTPUT=!BASENAME!_clip.%FORMAT%"
)

:: Build ffmpeg command
set FFMPEG_OPTS=-i "%INPUT%"

if not "%START_TIME%"=="" set FFMPEG_OPTS=%FFMPEG_OPTS% -ss %START_TIME%
if not "%END_TIME%"=="" (
    set FFMPEG_OPTS=%FFMPEG_OPTS% -to %END_TIME%
) else if not "%DURATION%"=="" (
    set FFMPEG_OPTS=%FFMPEG_OPTS% -t %DURATION%
)

if not "%RESOLUTION%"=="" set FFMPEG_OPTS=%FFMPEG_OPTS% -vf "scale=%RESOLUTION%:force_original_aspect_ratio=decrease,pad=%RESOLUTION%:(ow-iw)/2:(oh-ih)/2"
if not "%SPEED%"=="" set FFMPEG_OPTS=%FFMPEG_OPTS% -filter:v "setpts=%SPEED%*PTS" -filter:a "atempo=%SPEED%"
if "%MUTE%"=="1" set FFMPEG_OPTS=%FFMPEG_OPTS% -an

:: Use fast encoding for quick clips
set FFMPEG_OPTS=%FFMPEG_OPTS% -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k

echo [视频剪辑] 正在处理...
echo 输入: %INPUT%
echo 输出: %OUTPUT%
echo.

ffmpeg %FFMPEG_OPTS% "%OUTPUT%"

if %ERRORLEVEL%==0 (
    echo.
    echo 剪辑完成: %OUTPUT%
) else (
    echo.
    echo 剪辑失败
    exit /b 1
)
