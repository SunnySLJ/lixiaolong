@echo off
chcp 65001 >nul
echo ================================================
echo   Browser-Use 快速启动
echo ================================================
echo.
echo 选择运行模式:
echo.
echo 1. 运行测试脚本
echo 2. 交互式 CLI
echo 3. 查看帮助
echo.
set /p choice="请输入选项 (1-3): "

if "%choice%"=="1" (
    echo.
    echo 运行测试脚本...
    uv run python test_browser_use.py
) else if "%choice%"=="2" (
    echo.
    echo 启动交互式 CLI...
    uvx browser-use
) else if "%choice%"=="3" (
    echo.
    echo 查看帮助...
    uvx browser-use --help
) else (
    echo.
    echo 无效选项
)

pause
