@echo off
chcp 65001 >nul
echo ============================================================
echo 抖音发布工具 v0.2.0 - 快速安装
echo ============================================================
echo.
echo 正在安装 Python 依赖...
echo.

pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ============================================================
    echo 依赖安装失败！
    echo ============================================================
    echo.
    echo 请手动运行：pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo 安装完成！
echo ============================================================
echo.
echo 下一步:
echo.
echo 1. 启动 Web 管理界面
echo    streamlit run web_ui.py
echo.
echo 2. 配置官方 API 或网页自动化
echo.
echo 3. 开始发布视频
echo.
echo 详细文档：README_V2.md
echo ============================================================
pause
