"""
测试抖音上传页面 - 查找正确的上传入口
"""

import asyncio
import sys
import json
from playwright.async_api import async_playwright

async def find_upload_page():
    """查找抖音上传页面"""
    
    print("=" * 60)
    print("查找抖音上传页面")
    print("=" * 60)
    print()
    
    # 加载 Cookie
    cookie_file = "./storage/cookies/default.json"
    with open(cookie_file, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    print(f"已加载 Cookie：{len(cookies)} 个")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        context = await browser.new_context()
        await context.add_cookies(cookies)
        
        page = await context.new_page()
        
        # 尝试多个可能的上传页面 URL
        urls = [
            "https://creator.douyin.com/upload",
            "https://creator.douyin.com/creator-micro/upload",
            "https://creator.douyin.com/creator-micro/home",
            "https://www.douyin.com/upload",
        ]
        
        for url in urls:
            print(f"\n尝试：{url}")
            await page.goto(url, timeout=30000)
            await asyncio.sleep(3)
            
            # 截图
            filename = f"debug_{url.split('/')[-1]}.png"
            await page.screenshot(path=filename)
            print(f"已保存截图：{filename}")
            
            # 查找上传按钮
            upload_selectors = [
                'input[type="file"]',
                'button:has-text("上传视频")',
                'button:has-text("发布视频")',
                'a[href*="upload"]',
                '[data-e2e="upload-btn"]',
            ]
            
            for selector in upload_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        print(f"✓ 找到上传元素：{selector}")
                        text = await element.inner_text()
                        print(f"  文本：{text}")
                except:
                    pass
            
            # 打印当前 URL
            print(f"当前 URL: {page.url}")
        
        # 保持浏览器打开，让人工检查
        print("\n浏览器保持打开状态，请人工检查哪个是正确的上传页面")
        print("按 Ctrl+C 退出")
        
        try:
            await asyncio.sleep(60)
        except KeyboardInterrupt:
            pass
        
        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(find_upload_page())
