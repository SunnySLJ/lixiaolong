"""
发布视频并验证结果
"""

import asyncio
import sys
import json
from playwright.async_api import async_playwright

async def publish_and_verify():
    """发布视频并验证是否真的成功"""
    
    print("=" * 60)
    print("抖音发布工具 - 发布并验证")
    print("=" * 60)
    print()
    
    # 视频信息
    video_path = "./storage/videos/test.mp4"
    title = "AI 自动化测试视频"
    description = "使用抖音发布工具自动上传 #AI #自动化 #科技前沿"
    
    print(f"视频：{video_path}")
    print(f"标题：{title}")
    print(f"描述：{description}")
    print()
    
    # 加载 Cookie
    cookie_file = "./storage/cookies/default.json"
    with open(cookie_file, 'r', encoding='utf-8') as f:
        cookies = json.load(f)
    print(f"已加载 Cookie：{len(cookies)} 个")
    
    result = {"success": False, "message": "", "video_url": ""}
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                channel="chrome",
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            context = await browser.new_context()
            await context.add_cookies(cookies)
            
            page = await context.new_page()
            
            # 1. 导航到上传页面
            print("正在打开上传页面...")
            await page.goto("https://creator.douyin.com/creator-micro/content/upload", timeout=60000)
            await asyncio.sleep(5)
            print("✓ 上传页面已打开")
            
            # 截图
            await page.screenshot(path="debug_01_upload_page.png")
            print("已截图：debug_01_upload_page.png")
            
            # 2. 上传视频
            print("\n正在上传视频...")
            video_input = await page.query_selector('input[type="file"]')
            
            if not video_input:
                print("❌ 未找到上传按钮")
                await page.screenshot(path="debug_02_no_upload.png")
                print("当前页面 URL:", page.url)
                print("已截图：debug_02_no_upload.png")
                await context.close()
                await browser.close()
                return
            
            await video_input.set_input_files(video_path)
            print("✓ 视频文件已选择")
            
            # 等待视频上传和处理
            print("等待视频上传和处理...")
            for i in range(10, 0, -1):
                print(f"  等待中... {i}s")
                await asyncio.sleep(1)
            
            # 截图
            await page.screenshot(path="debug_03_video_uploaded.png")
            print("已截图：debug_03_video_uploaded.png")
            
            # 3. 设置标题
            print("\n正在设置标题...")
            title_input = await page.query_selector('input[placeholder*="标题"]')
            if title_input:
                await title_input.fill(title)
                print("✓ 标题已设置")
            else:
                print("⚠ 未找到标题输入框")
            
            # 4. 设置描述
            print("\n正在设置描述...")
            desc_selectors = [
                'textarea[placeholder*="描述"]',
                'textarea[placeholder*="文案"]',
                'div[contenteditable="true"]',
                '[data-e2e="desc-input"]'
            ]
            
            desc_input = None
            for selector in desc_selectors:
                try:
                    desc_input = await page.query_selector(selector)
                    if desc_input:
                        print(f"✓ 找到描述输入框：{selector}")
                        await desc_input.fill(description)
                        print("✓ 描述已设置")
                        break
                except:
                    pass
            
            if not desc_input:
                print("⚠ 未找到描述输入框，跳过")
            
            # 截图
            await page.screenshot(path="debug_04_info_filled.png")
            print("已截图：debug_04_info_filled.png")
            
            # 5. 等待并发布
            print("\n等待页面元素加载...")
            await asyncio.sleep(3)
            
            # 查找发布按钮
            print("正在查找发布按钮...")
            publish_selectors = [
                'button:has-text("发布")',
                'button:has-text("发表")',
                'button:has-text("下一步")',
                '[data-e2e="publish-btn"]',
                '.publish-btn'
            ]
            
            publish_button = None
            for selector in publish_selectors:
                try:
                    publish_button = await page.query_selector(selector)
                    if publish_button:
                        print(f"✓ 找到发布按钮：{selector}")
                        break
                except:
                    pass
            
            if publish_button:
                print("点击发布按钮...")
                await publish_button.click()
                
                # 等待发布完成
                print("等待发布完成...")
                for i in range(15, 0, -1):
                    print(f"  等待中... {i}s")
                    await asyncio.sleep(1)
                
                # 截图
                await page.screenshot(path="debug_05_after_publish.png")
                print("已截图：debug_05_after_publish.png")
                
                # 检查是否发布成功
                current_url = page.url
                print(f"\n当前 URL: {current_url}")
                
                # 检查是否有成功提示
                if "success" in current_url.lower() or "content" in current_url.lower():
                    result["success"] = True
                    result["message"] = "发布成功"
                    print("✅ 发布成功！")
                else:
                    # 检查页面是否有错误提示
                    error_text = await page.content()
                    if "失败" in error_text or "错误" in error_text:
                        result["message"] = "页面显示错误"
                        print("❌ 页面显示错误")
                    else:
                        result["message"] = "未确认发布成功"
                        print("⚠️ 未确认发布成功")
            else:
                print("❌ 未找到发布按钮")
                result["message"] = "未找到发布按钮"
            
            await context.close()
            await browser.close()
            
    except Exception as e:
        print(f"❌ 发布过程出错：{e}")
        result["message"] = str(e)
    
    print()
    print("=" * 60)
    print("发布结果:")
    print(f"  状态：{'✅ 成功' if result['success'] else '❌ 失败'}")
    print(f"  消息：{result['message']}")
    print("=" * 60)
    print()
    print("调试截图已保存:")
    print("  - debug_01_upload_page.png")
    print("  - debug_02_no_upload.png (如有问题)")
    print("  - debug_03_video_uploaded.png")
    print("  - debug_04_info_filled.png")
    print("  - debug_05_after_publish.png")
    print()
    print("请查看截图了解详细情况！")

if __name__ == "__main__":
    asyncio.run(publish_and_verify())
