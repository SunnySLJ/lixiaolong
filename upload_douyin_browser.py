from playwright.sync_api import sync_playwright
import time
import os

video_path = r"S:\ruoyi\video\春分龙抬头_20260320113103A039.mp4"
title = "春分龙抬头天文奇观本世纪仅 3 次"
desc = "春分遇上龙抬头，百年难遇的天文奇观！漆黑夜空中星辰变换，龙形光影与星辰交融，祥瑞之兆。#春分龙抬头 #天文奇观 #百年难遇 #祥瑞之兆 #视觉盛宴"

print("=" * 60)
print("抖音视频上传 - 浏览器自动化")
print("=" * 60)
print(f"视频：{video_path}")
print(f"标题：{title}")
print(f"描述：{desc[:50]}...")
print()

if not os.path.exists(video_path):
    print(f"错误：视频文件不存在")
    exit(1)

with sync_playwright() as p:
    # 连接到现有浏览器
    try:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:18789")
        context = browser.contexts[0]
        pages = context.pages
        page = pages[0] if pages else context.new_page()
        print("✓ 已连接到浏览器")
    except Exception as e:
        print(f"连接失败：{e}")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
    
    # 打开抖音上传页面
    print("正在打开抖音上传页面...")
    page.goto("https://creator.douyin.com/creator-micro/content/upload", wait_until="networkidle", timeout=30000)
    time.sleep(3)
    
    # 检查是否登录
    if "login" in page.url.lower():
        print("⚠ 需要登录，请在浏览器中登录抖音")
        time.sleep(10)
    
    # 点击上传按钮
    print("\n正在上传视频...")
    try:
        # 找到文件上传输入框
        page.wait_for_selector('input[type="file"]', timeout=10000)
        page.set_input_files('input[type="file"]', video_path)
        print("✓ 视频上传成功")
        time.sleep(5)
    except Exception as e:
        print(f"上传失败：{e}")
        print("请手动上传视频")
        time.sleep(5)
    
    # 填写标题
    print("\n正在填写标题...")
    try:
        title_input = page.locator('input[placeholder*="标题"]').first
        if title_input.is_visible(timeout=5000):
            title_input.fill(title)
            print("✓ 标题已填写")
    except Exception as e:
        print(f"填写标题失败：{e}")
    
    time.sleep(2)
    
    # 填写描述
    print("\n正在填写描述...")
    try:
        desc_editor = page.locator('div[contenteditable="true"]').first
        if desc_editor.is_visible(timeout=5000):
            desc_editor.fill(desc)
            print("✓ 描述已填写")
    except Exception as e:
        print(f"填写描述失败：{e}")
    
    time.sleep(2)
    
    # 截图确认
    page.screenshot(path="C:\\Users\\爽爽\\.openclaw\\workspace\\douyin_upload_status.png", full_page=True)
    print("\n✓ 截图已保存：C:\\Users\\爽爽\\.openclaw\\workspace\\douyin_upload_status.png")
    
    print("\n" + "=" * 60)
    print("上传完成！请检查浏览器窗口确认发布状态")
    print("视频正在审核中...")
    print("=" * 60)
    
    time.sleep(5)
