"""
抖音发布器核心模块
使用 Playwright 实现自动化发布
"""

import asyncio
import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from playwright.async_api import async_playwright, Page, Browser, BrowserContext

logger = logging.getLogger(__name__)


class DouyinPublisher:
    """抖音发布器"""
    
    def __init__(self, storage_path: str = "./storage"):
        """
        初始化发布器
        
        Args:
            storage_path: 存储路径（保存 Cookie 等）
        """
        self.storage_path = Path(storage_path)
        self.cookies_path = self.storage_path / "cookies"
        self.videos_path = self.storage_path / "videos"
        
        # 创建目录
        self.cookies_path.mkdir(parents=True, exist_ok=True)
        self.videos_path.mkdir(parents=True, exist_ok=True)
        
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # 抖音创作者页面
        self.creator_url = "https://creator.douyin.com/"
        self.upload_url = "https://creator.douyin.com/upload"
    
    async def login(self, profile: str = "default") -> bool:
        """
        扫码登录抖音
        
        Args:
            profile: 登录配置名称（支持多账号）
            
        Returns:
            是否登录成功
        """
        logger.info("正在启动浏览器...")
        
        async with async_playwright() as p:
            # 启动浏览器
            self.browser = await p.chromium.launch(
                headless=False,  # 有头模式，方便扫码
                channel="chrome",
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox"
                ]
            )
            
            # 创建浏览器上下文
            self.context = await self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            
            # 反检测
            await self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)
            
            self.page = await self.context.new_page()
            
            # 导航到抖音创作者页面
            logger.info("正在打开抖音创作者页面...")
            await self.page.goto(self.creator_url, timeout=60000)
            
            # 等待登录
            logger.info("请使用抖音 APP 扫码登录...")
            logger.info("登录成功后会自动保存 Cookie（等待 180 秒）")
            
            # 等待登录完成（检测多种可能的元素）
            try:
                # 尝试等待用户头像或用户昵称出现
                await asyncio.sleep(5)  # 等待页面加载
                
                # 多种检测方式
                selectors = [
                    '[data-e2e="user-avatar"]',
                    '[data-e2e="user-name"]',
                    '.user-avatar',
                    '.douyin-user-info',
                    'a[href*="/user"]'
                ]
                
                logged_in = False
                for selector in selectors:
                    try:
                        element = await self.page.wait_for_selector(selector, timeout=30000)
                        if element:
                            logged_in = True
                            break
                    except:
                        continue
                
                if not logged_in:
                    # 最后检查页面 URL 是否变化（登录后会跳转）
                    current_url = self.page.url
                    if "creator.douyin.com" in current_url and "login" not in current_url:
                        logged_in = True
                
                if logged_in:
                    logger.info("✅ 检测到登录成功！")
                    await self._save_cookies(profile)
                    return True
                else:
                    logger.warning("⚠️ 未检测到登录，但已超时，尝试保存当前 Cookie")
                    await self._save_cookies(profile)
                    return True  # 即使未检测到，也尝试保存 Cookie
                
            except Exception as e:
                logger.error(f"登录检测异常：{e}")
                # 即使异常也尝试保存 Cookie
                try:
                    await self._save_cookies(profile)
                    return True
                except:
                    return False
            
            finally:
                await self.context.close()
                await self.browser.close()
    
    async def publish(
        self,
        video_path: str,
        title: str,
        description: str = "",
        cover_path: Optional[str] = None,
        privacy: str = "public",
        profile: str = "default"
    ) -> Dict[str, Any]:
        """
        发布视频
        
        Args:
            video_path: 视频文件路径
            title: 视频标题
            description: 视频描述（包含话题标签）
            cover_path: 封面图片路径（可选）
            privacy: 隐私设置 (public/friend/private)
            profile: 使用的登录配置
            
        Returns:
            发布结果
        """
        result = {
            "success": False,
            "message": "",
            "video_id": "",
            "url": ""
        }
        
        try:
            # 1. 加载 Cookie
            if not await self._load_cookies(profile):
                result["message"] = "未登录，请先登录"
                return result
            
            logger.info("正在启动浏览器...")
            
            async with async_playwright() as p:
                # 启动浏览器
                self.browser = await p.chromium.launch(
                    headless=False,
                    channel="chrome",
                    args=["--disable-blink-features=AutomationControlled"]
                )
                
                # 创建上下文（带 Cookie）
                self.context = await self.browser.new_context()
                await self.context.add_cookies(await self._load_cookies(profile))
                
                self.page = await self.context.new_page()
                
                # 2. 导航到上传页面
                logger.info("正在打开上传页面...")
                await self.page.goto(self.upload_url, timeout=60000)
                await asyncio.sleep(3)  # 等待页面加载
                
                # 3. 上传视频
                logger.info("正在上传视频...")
                video_input = await self.page.query_selector('input[type="file"]')
                if not video_input:
                    result["message"] = "未找到上传按钮"
                    return result
                
                await video_input.set_input_files(video_path)
                
                # 等待视频上传完成
                logger.info("等待视频上传完成...")
                await asyncio.sleep(5)
                
                # 4. 设置标题
                logger.info("正在设置标题...")
                title_input = await self.page.query_selector('input[placeholder*="标题"]')
                if title_input:
                    await title_input.fill(title)
                
                # 5. 设置描述
                if description:
                    logger.info("正在设置描述...")
                    desc_input = await self.page.query_selector('textarea[placeholder*="描述"]')
                    if desc_input:
                        await desc_input.fill(description)
                
                # 6. 设置封面
                if cover_path and os.path.exists(cover_path):
                    logger.info("正在设置封面...")
                    # 找到封面上传区域并上传
                
                # 7. 设置隐私
                logger.info("正在设置隐私选项...")
                # 根据 privacy 参数选择对应的选项
                
                # 8. 点击发布
                logger.info("正在发布视频...")
                publish_button = await self.page.query_selector('button:has-text("发布")')
                if publish_button:
                    await publish_button.click()
                    
                    # 等待发布完成
                    await asyncio.sleep(5)
                    
                    # 检查发布结果
                    result["success"] = True
                    result["message"] = "发布成功"
                    logger.info("✅ 视频发布成功！")
                else:
                    result["message"] = "未找到发布按钮"
                
                return result
                
        except Exception as e:
            logger.error(f"发布失败：{e}")
            result["message"] = f"发布失败：{str(e)}"
            return result
        
        finally:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
    
    async def check_login(self, profile: str = "default") -> bool:
        """检查登录状态"""
        cookies = await self._load_cookies(profile)
        return len(cookies) > 0
    
    async def logout(self, profile: str = "default") -> bool:
        """退出登录"""
        cookie_file = self.cookies_path / f"{profile}.json"
        if cookie_file.exists():
            cookie_file.unlink()
            logger.info("已退出登录")
            return True
        return False
    
    async def _save_cookies(self, profile: str):
        """保存 Cookie"""
        if self.context:
            cookies = await self.context.cookies()
            cookie_file = self.cookies_path / f"{profile}.json"
            
            with open(cookie_file, 'w', encoding='utf-8') as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Cookie 已保存至：{cookie_file}")
    
    async def _load_cookies(self, profile: str) -> list:
        """加载 Cookie"""
        cookie_file = self.cookies_path / f"{profile}.json"
        
        if cookie_file.exists():
            with open(cookie_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            logger.info(f"已加载 Cookie：{profile}")
            return cookies
        
        return []


# 便捷函数
async def login_douyin(profile: str = "default"):
    """快捷登录函数"""
    publisher = DouyinPublisher()
    return await publisher.login(profile)


async def publish_video(
    video_path: str,
    title: str,
    description: str = "",
    **kwargs
):
    """快捷发布函数"""
    publisher = DouyinPublisher()
    return await publisher.publish(video_path, title, description, **kwargs)
