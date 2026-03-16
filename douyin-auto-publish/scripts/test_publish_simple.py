"""
发布测试视频 - 修复版
"""

import asyncio
import sys
import logging
import codecs
import json

if sys.platform == 'win32':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

sys.path.insert(0, '.')
from playwright.async_api import async_playwright

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

async def publish_video():
    """发布视频到抖音"""
    
    print("=" * 60)
    print("抖音发布工具 - 发布视频")
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
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        print(f"已加载 Cookie：{len(cookies)} 个")
    except Exception as e:
        print(f"未找到 Cookie，请先登录：python scripts/quick_login.py")
        return
    
    print()
    print("正在启动浏览器...")
    
    result = {"success": False, "message": ""}
    
    try:
        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(
                headless=False,
                channel="chrome",
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            # 创建上下文
            context = await browser.new_context()
            await context.add_cookies(cookies)
            
            page = await context.new_page()
            
            # 1. 导航到上传页面
            print("正在打开上传页面...")
            await page.goto("https://creator.douyin.com/creator-micro/content/upload", timeout=60000)
            await asyncio.sleep(5)  # 等待页面加载
            
            # 2. 上传视频
            print("正在上传视频...")
            video_input = await page.query_selector('input[type="file"]')
            
            if not video_input:
                print("❌ 未找到上传按钮")
                print("当前页面 URL:", page.url)
                
                # 尝试截图
                await page.screenshot(path="debug_upload_page.png")
                print("已保存截图：debug_upload_page.png")
                
                result["message"] = "未找到上传按钮"
                await context.close()
                await browser.close()
                return
            
            await video_input.set_input_files(video_path)
            print("✓ 视频文件已选择")
            
            # 等待视频上传
            print("等待视频上传完成...")
            await asyncio.sleep(10)  # 增加等待时间
            
            # 3. 设置标题
            print("正在设置标题...")
            title_input = await page.query_selector('input[placeholder*="标题"]')
            if title_input:
                await title_input.fill(title)
                print("✓ 标题已设置")
            else:
                print("⚠ 未找到标题输入框")
            
            # 4. 设置描述
            print("正在设置描述...")
            desc_input = await page.query_selector('textarea[placeholder*="描述"]')
            if desc_input:
                await desc_input.fill(description)
                print("✓ 描述已设置")
            else:
                print("⚠ 未找到描述输入框")
            
            # 5. 等待更长时间确保所有元素加载
            print("等待页面元素加载...")
            await asyncio.sleep(5)
            
            # 6. 查找发布按钮
            print("正在查找发布按钮...")
            publish_button = await page.query_selector('button:has-text("发布")')
            
            if publish_button:
                print("✓ 找到发布按钮，点击发布...")
                await publish_button.click()
                
                # 等待发布完成
                print("等待发布完成...")
                await asyncio.sleep(10)
                
                # 检查是否有成功提示
                result["success"] = True
                result["message"] = "发布成功"
                print("✅ 视频发布成功！")
            else:
                print("❌ 未找到发布按钮")
                result["message"] = "未找到发布按钮"
                
                # 截图调试
                await page.screenshot(path="debug_publish_button.png")
                print("已保存截图：debug_publish_button.png")
            
            # 清理
            await context.close()
            await browser.close()
            
    except Exception as e:
        print(f"❌ 发布失败：{e}")
        result["message"] = str(e)
    
    print()
    print("=" * 60)
    if result["success"]:
        print("🎉 发布成功！")
        print("请在抖音 APP 中查看视频")
    else:
        print(f"❌ 发布失败：{result['message']}")
        print()
        print("可能的原因:")
        print("1. Cookie 已过期 - 请重新登录：python scripts/quick_login.py")
        print("2. 页面结构变化 - 请检查抖音创作者页面")
        print("3. 网络问题 - 请检查网络连接")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(publish_video())
