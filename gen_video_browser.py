"""
使用 Playwright 通过浏览器自动化调用帧龙虾 API
"""
from playwright.sync_api import sync_playwright
import time
import os
import json

cover_path = r"C:\Users\爽爽\Desktop\图片\cover.jpg"
prompt = "春分龙抬头天文奇观，漆黑夜空中春分与龙抬头天象重合，光芒四射，星辰变换，龙形光影与星辰交融，祥瑞之兆，神龙现身"

print("=" * 60)
print("帧龙虾视频生成 - 浏览器自动化")
print("=" * 60)
print(f"封面：{cover_path}")
print(f"提示词：{prompt[:50]}...")
print()

if not os.path.exists(cover_path):
    print(f"错误：封面图片不存在")
    exit(1)

with sync_playwright() as p:
    # 连接到现有浏览器
    try:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:18789")
        context = browser.contexts[0]
        pages = context.pages
        page = pages[0] if pages else context.new_page()
        print("✓ 已连接到现有浏览器")
    except Exception as e:
        print(f"连接失败：{e}")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
    
    # 打开帧龙虾
    print("正在打开帧龙虾网站...")
    page.goto("https://aihuanying.com/", wait_until="networkidle", timeout=30000)
    time.sleep(2)
    
    # 检查登录状态
    if "个人中心" in page.content():
        print("✓ 已登录")
    else:
        print("⚠ 未检测到登录状态，可能需要手动登录")
    
    # 上传封面图片
    print(f"\n正在上传封面图片...")
    try:
        # 点击上传区域
        page.click('.ant-upload', timeout=5000)
        time.sleep(1)
        
        # 使用 file chooser
        page.wait_for_selector('input[type="file"]', timeout=5000)
        page.set_input_files('input[type="file"]', cover_path)
        print("✓ 图片上传成功")
        time.sleep(2)
    except Exception as e:
        print(f"上传失败：{e}")
        print("请手动上传图片")
        time.sleep(5)
    
    # 填写提示词
    print("\n正在填写视频描述...")
    page.fill('textarea[placeholder*="描述你想要生成的视频"]', prompt)
    print("✓ 提示词已填写")
    time.sleep(1)
    
    # 设置比例为 9:16
    print("\n设置视频比例...")
    try:
        page.click('.ant-select:has-text("16:9")')
        time.sleep(0.5)
        page.click('.ant-select-item:has-text("9:16")')
        print("✓ 比例已设置为 9:16")
    except:
        print("⚠ 比例设置失败，使用默认值")
    time.sleep(1)
    
    # 点击立即生成
    print("\n正在提交视频生成任务...")
    page.click('button:has-text("立即生成")')
    print("✓ 任务已提交")
    
    # 等待确认
    time.sleep(3)
    
    # 截图
    page.screenshot(path="C:\\Users\\爽爽\\.openclaw\\workspace\\video_submit_result.png", full_page=True)
    print("\n✓ 操作完成！")
    print("截图已保存：C:\\Users\\爽爽\\.openclaw\\workspace\\video_submit_result.png")
    print("\n视频正在生成中，请在网页上查看进度...")
    
    # 保持浏览器打开
    time.sleep(10)

print("=" * 60)
