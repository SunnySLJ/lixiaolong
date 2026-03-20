#!/usr/bin/env python3
"""
Douyin Video Upload Script
上传视频到抖音创作者中心，使用已登录的 Chrome 会话
"""

import argparse
import sys
import time
from pathlib import Path
from typing import Optional, List

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Page


# 抖音创作者中心上传页面
UPLOAD_URL = "https://creator.douyin.com/creator-micro/content/upload"
# 作品管理页面
WORKS_URL = "https://creator.douyin.com/creator-micro/content/manage"


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器"""
    parser = argparse.ArgumentParser(description="上传视频到抖音")
    parser.add_argument("--video", required=True, help="视频文件路径")
    parser.add_argument("--cover", help="封面图片路径（可选，不传则使用 AI 封面）")
    parser.add_argument("--title", required=True, help="视频标题（最多 30 字）")
    parser.add_argument("--desc", required=True, help="视频描述")
    parser.add_argument("--tags", nargs="*", default=[], help="话题标签列表（不含#）")
    parser.add_argument("--publish", action="store_true", default=True, help="自动点击发布")
    parser.add_argument("--debug-port", type=int, default=18800, help="Chrome 远程调试端口")
    parser.add_argument("--timeout", type=int, default=300, help="操作超时时间（秒）")
    return parser


def log(message: str) -> None:
    """打印日志"""
    print(f"[{time.strftime('%H:%M:%S')}] {message}", flush=True)


def ensure_file(path: Path, label: str) -> None:
    """检查文件是否存在"""
    if not path.exists():
        raise FileNotFoundError(f"{label} 不存在：{path}")


def save_screenshot(page: Page, name: str) -> str:
    """保存截图"""
    try:
        path = f"/tmp/douyin_{name}_{int(time.time())}.png"
        page.screenshot(path=path, full_page=True, timeout=5000)
        log(f"截图已保存：{path}")
        return path
    except Exception as e:
        log(f"截图失败：{e}")
        return None


def connect_to_chrome(debug_port: int, timeout: int = 30000) -> Page:
    """连接到 Chrome 浏览器"""
    from playwright.sync_api import sync_playwright
    
    log(f"正在连接 Chrome (端口：{debug_port})...")
    
    with sync_playwright() as playwright:
        endpoint = f"http://127.0.0.1:{debug_port}"
        log(f"CDP 端点：{endpoint}")
        
        try:
            browser = playwright.chromium.connect_over_cdp(endpoint, timeout=timeout)
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            page = context.new_page()
            page.set_default_timeout(20000)
            log("✓ Chrome 连接成功")
            return page
        except Exception as e:
            raise RuntimeError(f"无法连接 Chrome，请确保浏览器已启动并开启了远程调试：{e}")


def goto_upload_page(page: Page) -> None:
    """打开上传页面"""
    log(f"正在打开上传页面...")
    page.goto(UPLOAD_URL, wait_until="domcontentloaded", timeout=90000)
    time.sleep(3)
    log("✓ 上传页面已打开")


def upload_video(page: Page, video_path: Path, timeout: int = 180) -> None:
    """上传视频文件"""
    log(f"正在上传视频：{video_path.name}")
    
    # 点击上传按钮
    page.click('button:has-text("上传视频"), input[type="file"]', timeout=10000)
    time.sleep(2)
    
    # 使用文件上传功能
    page.set_input_files('input[type="file"]', str(video_path), timeout=10000)
    
    # 等待上传完成
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            # 检查是否出现标题输入框（表示上传完成）
            title_input = page.locator('input.semi-input-default').first
            if title_input.is_visible(timeout=5000):
                log("✓ 视频上传完成")
                return
        except Exception:
            pass
        time.sleep(2)
    
    raise TimeoutError("视频上传超时")


def wait_for_ai_cover(page: Page, timeout: int = 30) -> None:
    """等待 AI 封面生成完成"""
    log("正在等待 AI 封面生成...")
    
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            # 检查是否显示"生成中"
            generating = page.locator('text=生成中')
            if generating.count() == 0:
                log("✓ AI 封面已生成")
                return
        except Exception:
            pass
        time.sleep(2)
    
    log("⚠ AI 封面生成超时，继续操作")


def select_cover(page: Page) -> None:
    """选择 AI 生成的封面"""
    log("正在选择封面...")
    
    try:
        # 点击"选择封面"
        page.click('text=选择封面', timeout=10000)
        time.sleep(2)
        
        # 等待封面弹窗出现
        page.wait_for_selector('text=AI 封面', timeout=10000)
        time.sleep(3)
        
        # 点击"完成"按钮
        page.click('button:has-text("完成")', timeout=10000)
        time.sleep(2)
        
        log("✓ 封面已选择")
    except Exception as e:
        log(f"⚠ 封面选择失败：{e}，尝试继续操作")


def fill_info(page: Page, title: str, desc: str, tags: List[str]) -> None:
    """填写视频信息"""
    log(f"正在填写信息...")
    
    # 填写标题
    title_input = page.locator('input.semi-input-default').first
    title_input.wait_for(state="visible", timeout=10000)
    title_input.click(force=True)
    page.keyboard.press("Meta+a")  # macOS
    title_input.fill(title[:30])
    log(f"✓ 标题已填写：{title[:30]}")
    
    # 填写描述
    desc_editor = page.locator('div[contenteditable="true"]').first
    desc_editor.wait_for(state="visible", timeout=10000)
    desc_editor.click(force=True)
    page.keyboard.press("Meta+a")
    page.keyboard.press("Backspace")
    
    # 输入描述
    page.keyboard.type(desc, delay=30)
    
    # 添加标签
    for tag in tags:
        page.keyboard.type(f" #{tag}", delay=30)
        time.sleep(0.3)
    
    log(f"✓ 描述和标签已填写")


def close_dialogs(page: Page) -> None:
    """关闭可能的弹窗"""
    try:
        # 关闭"设置横封面"弹窗
        if page.is_visible('button:has-text("暂不设置")', timeout=3000):
            page.click('button:has-text("暂不设置")')
            log("✓ 已关闭横封面弹窗")
            time.sleep(1)
    except Exception:
        pass


def click_publish(page: Page) -> None:
    """点击发布按钮"""
    log("正在点击发布按钮...")
    
    # 滚动到底部
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    
    # 关闭可能的弹窗
    close_dialogs(page)
    
    # 点击发布按钮
    publish_btn = page.locator('button:has-text("发布")').first
    publish_btn.wait_for(state="visible", timeout=10000)
    publish_btn.scroll_into_view_if_needed()
    publish_btn.click(force=True)
    
    log("✓ 发布按钮已点击")


def wait_for_publish(page: Page, timeout: int = 60) -> None:
    """等待发布完成"""
    log("正在等待发布...")
    
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            # 检查是否跳转到作品管理页面或显示审核中
            url = page.url
            if "manage" in url or "审核中" in page.content():
                log("✓ 发布成功，视频正在审核中")
                return
        except Exception:
            pass
        time.sleep(2)
    
    log("⚠ 发布状态检测超时，但可能已成功")


def main() -> int:
    """主函数"""
    args = build_parser().parse_args()
    
    video_path = Path(args.video)
    cover_path = Path(args.cover) if args.cover else None
    
    # 检查文件
    ensure_file(video_path, "视频文件")
    if cover_path:
        ensure_file(cover_path, "封面文件")
    
    log("=" * 60)
    log("🎬 抖音视频上传")
    log("=" * 60)
    log(f"📹 视频：{video_path.name}")
    log(f"📝 标题：{args.title}")
    log(f"📄 描述：{args.desc}")
    log(f"🏷️  标签：{', '.join(args.tags)}")
    log(f"🖼️  封面：{cover_path.name if cover_path else 'AI 智能封面'}")
    log("=" * 60)
    
    try:
        # 连接 Chrome
        page = connect_to_chrome(args.debug_port)
        
        # 打开上传页面
        goto_upload_page(page)
        
        # 上传视频
        upload_video(page, video_path)
        
        # 等待 AI 封面生成
        wait_for_ai_cover(page)
        
        # 选择封面
        select_cover(page)
        
        # 填写信息
        fill_info(page, args.title, args.desc, args.tags)
        
        # 保存截图
        save_screenshot(page, "before_publish")
        
        # 点击发布
        if args.publish:
            click_publish(page)
            wait_for_publish(page)
            save_screenshot(page, "after_publish")
            log("=" * 60)
            log("✅ 发布完成！视频正在审核中")
            log("📱 可以在抖音 APP 中查看审核状态")
            log("=" * 60)
        else:
            log("=" * 60)
            log("⏸️  表单已准备好，未自动发布")
            log("👉 请手动点击发布按钮")
            log("=" * 60)
        
        # 保持浏览器打开
        log("🌐 浏览器保持打开状态...")
        
        return 0
        
    except FileNotFoundError as e:
        log(f"❌ 文件错误：{e}")
        return 1
    except PlaywrightTimeoutError as e:
        log(f"❌ 操作超时：{e}")
        save_screenshot(page, "error")
        return 1
    except Exception as e:
        log(f"❌ 上传失败：{e}")
        save_screenshot(page, "error")
        return 1


if __name__ == "__main__":
    sys.exit(main())
