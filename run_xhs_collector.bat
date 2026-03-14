@echo off
chcp 65001 >nul
echo ========================================
echo 智小红 - 小红书数据自动采集分析
echo ========================================
echo.
echo 本脚本将:
echo 1. 打开浏览器自动采集小红书热点
echo 2. 自动导出数据 (JSON/Excel/CSV)
echo 3. 自动生成分析报告
echo.
echo 注意:
echo - 需要手动登录一次小红书
echo - 每条笔记间隔 6 秒 (防风控)
echo - 建议用小号操作
echo.
pause
echo.
echo 正在安装依赖...
pip install playwright pandas openpyxl -q
echo.
echo 正在启动浏览器...
python xiaohongshu_collector.py
echo.
echo 正在分析数据...
python xhs_analyzer.py
echo.
echo ========================================
echo 完成！
echo ========================================
echo.
echo 数据位置：xhs_data\
echo.
echo 查看报告:
echo   - analysis_report_*.txt (详细报告)
echo   - xhs_data_*.xlsx (Excel 数据)
echo.
pause
