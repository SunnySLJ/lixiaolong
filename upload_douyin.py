"""Upload video to Douyin using existing browser session"""
import asyncio
from playwright.async_api import async_playwright

async def main():
    video_path = r"C:\Users\爽爽\.openclaw\workspace\test_video.mp4"
    title = "春日随拍小片段｜城市日常记录"
    desc = "今天随手记录一段生活片段，节奏轻松，画面干净，适合当作日常更新。"
    tags = ["日常记录", "生活碎片", "随拍", "vlog"]
    
    async with async_playwright() as p:
        # Connect to existing Chrome instance
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:18789")
        context = browser.contexts[0]
        page = context.pages[0]
        
        print(f"Current page: {page.url}")
        
        # Navigate to upload page if needed
        if "upload" not in page.url:
            await page.goto("https://creator.douyin.com/creator-micro/content/upload")
            await page.wait_for_load_state("networkidle")
        
        # Wait for file input to be available
        print("Waiting for file input...")
        file_input = page.locator('input[type="file"]').first
        await file_input.wait_for(state="attached", timeout=30000)
        
        # Upload video
        print(f"Uploading video: {video_path}")
        await file_input.set_input_files(video_path)
        
        # Wait for upload to complete
        await page.wait_for_timeout(5000)
        print("Video upload initiated!")
        
        # Fill title
        title_input = page.locator('input[placeholder*="标题"], input[aria-label*="标题"]').first
        if await title_input.count() > 0:
            await title_input.fill(title)
            print(f"Title filled: {title}")
        
        # Fill description
        desc_input = page.locator('div[contenteditable="true"], textarea[placeholder*="描述"]').first
        if await desc_input.count() > 0:
            await desc_input.fill(desc)
            print(f"Description filled: {desc}")
        
        # Add tags
        for tag in tags:
            # Try to find tag input and add tag
            print(f"Would add tag: {tag}")
        
        print("\nUpload in progress. You can continue manually or wait for auto-publish.")
        print("Browser will remain open.")

if __name__ == "__main__":
    asyncio.run(main())
