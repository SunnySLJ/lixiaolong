#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xiaohongshu Video Upload Script
上传视频到小红书创作平台，使用已登录的 Chrome 会话
"""

import argparse
import sys
import io
import time
from pathlib import Path

# 设置标准输出为 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Page

# 小红书创作中心上传页面
UPLOAD_URL = "https://creator.xiaohongshu.com/publish/publish"
HOME_URL = "https://creator.xiaohongshu.com/new/home"


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器"""
    parser = argparse.ArgumentParser(description="上传视频到小红书")
    parser.add_argument("--video", required=True, help="视频文件路径")
    parser.add_argument("--title", required=True, help="视频标题")
    parser.add_argument("--desc", required=True, help="视频描述")
    parser.add_argument("--tags", nargs="*", default=[], help="话题标签列表（不含#）")
    parser.add_argument("--debug-port", type=int, default=18800, help="Chrome 远程调试端口")
    parser.add_argument("--timeout", type=int, default=300, help="操作超时时间（秒）")
    return parser


def log(message: str) -> None:
    """打印日志"""
    # 移除所有 emoji 字符
    clean_msg = ''.join(c for c in message if ord(c) < 0x10000)
    print(f"[{time.strftime('%H:%M:%S')}] {clean_msg}", flush=True)


def ensure_file(path: Path, label: str) -> None:
    """检查文件是否存在"""
    if not path.exists():
        raise FileNotFoundError(f"{label} 不存在：{path}")


def save_screenshot(page: Page, name: str) -> str:
    """保存截图"""
    try:
        path = f"C:/Users/爽爽/.openclaw/workspace/xiaohongshu_{name}_{int(time.time())}.png"
        page.screenshot(path=path, full_page=True, timeout=5000)
        log(f"截图已保存：{path}")
        return path
    except Exception as e:
        log(f"截图失败：{e}")
        return None


def connect_to_chrome(debug_port: int, timeout: int = 30000):
    """连接到 Chrome 浏览器，不关闭现有窗口"""
    from playwright.sync_api import sync_playwright
    
    log(f"正在连接 Chrome (端口：{debug_port})...")
    
    playwright = sync_playwright().start()
    endpoint = f"http://127.0.0.1:{debug_port}"
    log(f"CDP 端点：{endpoint}")
    
    # 连接到现有 Chrome（不关闭）
    browser = playwright.chromium.connect_over_cdp(endpoint, timeout=timeout)
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    
    # 查找已有的小红书页面，如果没有则新建
    page = None
    for p in context.pages:
        if "creator.xiaohongshu.com" in p.url:
            page = p
            log("✓ 找到已有的小红书页面")
            break
    
    if not page:
        page = context.new_page()
        log("✓ 创建新页面")
    
    page.set_default_timeout(60000)
    log("✓ Chrome 连接成功")
    return playwright, browser, page


def goto_upload_page(page: Page) -> None:
    """打开上传页面 - 不关闭现有浏览器窗口"""
    log(f"正在打开上传页面...")
    
    # 检查当前页面是否已经是上传页面
    if "publish/publish" in page.url:
        log("✓ 已在上传页面")
        time.sleep(2)
        return
    
    # 导航到上传页面
    page.goto(UPLOAD_URL, wait_until="domcontentloaded", timeout=90000)
    time.sleep(3)
    log("✓ 上传页面已打开")


def upload_video(page: Page, video_path: Path, timeout: int = 180) -> None:
    """上传视频文件"""
    log(f"正在上传视频：{video_path.name}")
    
    # 等待页面加载
    page.wait_for_load_state("networkidle", timeout=30000)
    time.sleep(3)
    
    # 查找文件上传按钮
    try:
        # 点击"选择文件"按钮
        upload_btn = page.locator('button:has-text("选择文件"), button:has-text("上传视频")').first
        upload_btn.wait_for(state="visible", timeout=10000)
        upload_btn.click(timeout=5000)
        log("✓ 已点击上传按钮")
        time.sleep(2)
    except Exception as e:
        log(f"点击上传按钮失败：{e}")
    
    # 查找文件输入框并上传
    try:
        file_input = page.locator('input[type="file"]').first
        file_input.wait_for(state="attached", timeout=10000)
        file_input.set_input_files(str(video_path), timeout=60000)
        log("✓ 视频文件已选择")
    except Exception as e:
        log(f"上传文件失败：{e}")
        raise
    
    # 等待上传完成
    time.sleep(5)
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            # 检查是否出现标题输入框（表示上传完成）
            title_input = page.locator('input[placeholder*="标题"]').first
            if title_input.is_visible(timeout=3000):
                log("✓ 视频上传完成")
                return
        except:
            pass
        time.sleep(3)
    
    log("⚠ 视频上传可能仍在进行中")


def fill_info(page: Page, title: str, desc: str, tags: list) -> None:
    """填写标题和描述"""
    log(f"正在填写信息...")
    
    # 填写标题
    try:
        title_input = page.locator('input[placeholder*="标题"]').first
        title_input.wait_for(state="visible", timeout=10000)
        title_input.fill(title[:20])
        log(f"✓ 标题已填写：{title[:20]}")
    except Exception as e:
        log(f"填写标题失败：{e}")
    
    time.sleep(1)
    
    # 填写描述和标签
    try:
        desc_input = page.locator('textarea[placeholder*="描述"]').first
        desc_input.wait_for(state="visible", timeout=10000)
        
        # 输入描述
        desc_input.fill(desc)
        
        # 添加标签
        for tag in tags:
            desc_input.type(f" #{tag}")
            time.sleep(0.3)
        
        log(f"✓ 描述和标签已填写")
    except Exception as e:
        log(f"填写描述失败：{e}")


def click_publish(page: Page) -> None:
    """点击发布按钮"""
    log("正在点击发布按钮...")
    
    # 滚动到底部
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(2)
    
    # 点击发布按钮
    try:
        publish_btn = page.locator('button:has-text("发布")').first
        publish_btn.wait_for(state="visible", timeout=10000)
        publish_btn.scroll_into_view_if_needed()
        publish_btn.click(force=True)
        log("✓ 发布按钮已点击")
    except Exception as e:
        log(f"点击发布按钮失败：{e}")


def wait_for_publish(page: Page, timeout: int = 60) -> None:
    """等待发布完成"""
    log("正在等待发布...")
    
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            # 检查是否返回上传页或显示成功提示
            url = page.url
            if "publish" in url or "success" in page.content().lower():
                log("✓ 发布成功！")
                return
        except Exception:
            pass
        time.sleep(2)
    
    log("⚠ 发布状态检测超时，但可能已成功")


def main() -> int:
    """主函数"""
    args = build_parser().parse_args()
    
    video_path = Path(args.video)
    
    # 检查文件
    ensure_file(video_path, "视频文件")
    
    log("=" * 60)
    log("小红书视频上传")
    log("=" * 60)
    log(f"视频：{video_path.name}")
    log(f"标题：{args.title}")
    log(f"描述：{args.desc}")
    log(f"标签：{', '.join(args.tags)}")
    log("=" * 60)
    
    playwright = None
    browser = None
    page = None
    
    try:
        # 连接 Chrome
        playwright, browser, page = connect_to_chrome(args.debug_port)
        
        # 打开上传页面
        goto_upload_page(page)
        
        # 上传视频
        upload_video(page, video_path)
        
        # 填写信息
        fill_info(page, args.title, args.desc, args.tags)
        
        # 保存截图
        save_screenshot(page, "before_publish")
        
        # 点击发布
        click_publish(page)
        
        # 等待发布
        wait_for_publish(page)
        
        # 保存截图
        save_screenshot(page, "after_publish")
        
        log("=" * 60)
        log("发布完成！")
        log("可以在小红书 APP 中查看发布状态")
        log("=" * 60)
        
        # 保持浏览器打开
        log("浏览器保持打开状态...")
        
        return 0
        
    except FileNotFoundError as e:
        log(f"文件错误：{e}")
        return 1
    except PlaywrightTimeoutError as e:
        log(f"操作超时：{e}")
        if page:
            save_screenshot(page, "error")
        return 1
    except Exception as e:
        log(f"上传失败：{e}")
        if page:
            save_screenshot(page, "error")
        return 1
    finally:
        # 只关闭 Playwright 连接，保持 Chrome 浏览器打开
        if playwright:
            try:
                playwright.stop()
                log("✓ Playwright 已断开，浏览器保持打开")
            except:
                pass


if __name__ == "__main__":
    sys.exit(main())
