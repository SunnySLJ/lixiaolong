"""
使用 Playwright 通过浏览器自动化上传封面并生成视频
"""
from playwright.sync_api import sync_playwright
import time
import os

cover_path = r"C:\Users\爽爽\Desktop\图片\cover.jpg"
prompt = "春分龙抬头天文奇观，漆黑夜空中春分与龙抬头天象重合，光芒四射，星辰变换，龙形光影与星辰交融，祥瑞之兆，神龙现身"

print("=" * 60)
print("正在通过浏览器自动化上传封面并生成视频...")
print("=" * 60)
print(f"封面图片：{cover_path}")
print(f"提示词：{prompt[:50]}...")
print()

# 检查文件
if not os.path.exists(cover_path):
    print(f"错误：封面图片不存在：{cover_path}")
    exit(1)

with sync_playwright() as p:
    # 连接到现有浏览器会话
    try:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:18789")
    except Exception as e:
        print(f"无法连接浏览器：{e}")
        print("尝试启动新浏览器...")
        browser = p.chromium.launch(headless=False)
    
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    pages = context.pages
    
    if pages:
        page = pages[0]
    else:
        page = context.new_page()
    
    # 打开帧龙虾网站
    print("正在打开帧龙虾网站...")
    page.goto("https://aihuanying.com/", wait_until="networkidle", timeout=30000)
    time.sleep(2)
    
    # 点击参考图上传按钮
    print("正在点击上传按钮...")
    page.click('button:has-text("参考图")', timeout=10000)
    time.sleep(1)
    
    # 处理文件选择
    print(f"正在上传封面图片：{cover_path}")
    try:
        # 等待文件选择器出现
        page.wait_for_selector('input[type="file"]', timeout=5000)
        page.set_input_files('input[type="file"]', cover_path)
        print("✓ 图片上传成功")
    except Exception as e:
        print(f"文件上传失败：{e}")
        print("请手动上传图片")
    
    time.sleep(2)
    
    # 填写提示词
    print("正在填写视频描述...")
    page.fill('textarea[placeholder*="描述你想要生成的视频"]', prompt)
    print("✓ 提示词已填写")
    
    time.sleep(1)
    
    # 选择视频比例
    print("设置视频比例为 9:16 竖屏...")
    page.click('text=16:9 横屏')
    time.sleep(0.5)
    page.click('text=9:16 竖屏')
    print("✓ 比例已设置")
    
    time.sleep(1)
    
    # 点击立即生成
    print("正在提交视频生成任务...")
    page.click('button:has-text("立即生成")')
    print("✓ 任务已提交")
    
    # 等待确认
    time.sleep(3)
    
    # 截图保存当前状态
    page.screenshot(path="C:\\Users\\爽爽\\.openclaw\\workspace\\video_submit_result.png", full_page=True)
    print("\n✓ 操作完成！")
    print("请查看浏览器窗口确认视频生成状态")
    print("截图已保存：C:\\Users\\爽爽\\.openclaw\\workspace\\video_submit_result.png")
    
    # 保持浏览器打开
    print("\n浏览器将保持打开状态，视频正在生成中...")
    time.sleep(10)

print("=" * 60)
