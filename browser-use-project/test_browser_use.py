"""
Browser-Use 测试脚本
"""

from browser_use import Agent, Browser, ChatBrowserUse
import asyncio

async def main():
    print("🌐 Browser-Use 测试开始...\n")
    
    browser = Browser()
    
    agent = Agent(
        task="访问 GitHub 并搜索 browser-use 项目，告诉我它的 star 数量",
        llm=ChatBrowserUse(),
        browser=browser,
    )
    
    result = await agent.run()
    print(f"\n✅ 完成！结果：{result}")

if __name__ == "__main__":
    asyncio.run(main())
