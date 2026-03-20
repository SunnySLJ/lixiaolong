import argparse
import json
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


DEFAULT_VIDEO = Path(r"C:\Users\爽爽\Desktop\图片\2.mp4")
DEFAULT_COVER = Path(r"C:\Users\爽爽\Desktop\图片\2.cover.jpg")
SKILL_DIR = Path(__file__).resolve().parent.parent
COOKIE_FILE = SKILL_DIR / "douyin_cookies.json"
SCREENSHOT_DIR = SKILL_DIR
BROWSER_PROFILE_DIR = SCREENSHOT_DIR / ".browser-profile"

DEFAULT_TITLE = "春日随拍小片段｜城市日常记录"
DEFAULT_DESC = "今天随手记录一段生活片段，节奏轻松，画面干净，适合当作日常更新。"
DEFAULT_TAGS = ["日常记录", "生活碎片", "随拍", "vlog"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Douyin uploader debug script")
    parser.add_argument("--video", default=str(DEFAULT_VIDEO), help="video file path")
    parser.add_argument("--cover", default=str(DEFAULT_COVER), help="cover image path")
    parser.add_argument("--title", default=DEFAULT_TITLE, help="title text")
    parser.add_argument("--desc", default=DEFAULT_DESC, help="description text")
    parser.add_argument("--tags", nargs="*", default=DEFAULT_TAGS, help="topic tags without #")
    parser.add_argument("--publish", action="store_true", help="click publish button after form is filled")
    parser.add_argument(
        "--publish-wait-seconds",
        type=int,
        default=900,
        help="max seconds to wait for upload/checking to finish before clicking publish",
    )
    parser.add_argument("--headless", action="store_true", help="run browser in headless mode")
    parser.add_argument("--close-browser", action="store_true", help="close browser automatically when finished")
    parser.add_argument(
        "--use-existing-chrome",
        action="store_true",
        help="connect to existing Chrome with logged-in session (default behavior)",
    )
    parser.add_argument(
        "--debug-port",
        type=int,
        default=None,
        help="Chrome remote debugging port (default: auto-detect)",
    )
    return parser


def log(message: str) -> None:
    print(message, flush=True)


def find_browser_executable() -> Path:
    candidates = [
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError("Chrome/Edge executable not found")


def find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        sock.listen(1)
        return int(sock.getsockname()[1])


def launch_detached_browser() -> tuple[subprocess.Popen, str]:
    """启动新的 Chrome 实例（带调试端口）"""
    browser_path = find_browser_executable()
    port = find_free_port()
    BROWSER_PROFILE_DIR.mkdir(exist_ok=True)
    command = [
        str(browser_path),
        f"--remote-debugging-port={port}",
        f"--user-data-dir={BROWSER_PROFILE_DIR}",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-blink-features=AutomationControlled",
        "about:blank",
    ]
    creationflags = 0
    if sys.platform.startswith("win"):
        creationflags = subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS
    process = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=creationflags,
        close_fds=True,
    )
    endpoint = f"http://127.0.0.1:{port}"
    return process, endpoint


def find_existing_chrome_debug_port() -> int | None:
    """查找已运行的 Chrome 调试端口（默认 9222）"""
    import psutil
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'chrome' in proc.info['name'].lower() or 'chromium' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if '--remote-debugging-port=' in cmdline:
                    match = re.search(r'--remote-debugging-port=(\d+)', cmdline)
                    if match:
                        port = int(match.group(1))
                        log(f"[..] 发现已运行的 Chrome，调试端口：{port}")
                        return port
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


def connect_to_existing_chrome(playwright, port: int = None) -> tuple:
    """连接到用户已登录的 Chrome 浏览器"""
    if port is None:
        port = find_existing_chrome_debug_port()
    
    if port is None:
        # 如果没有找到已运行的 Chrome，启动一个新的
        log("[..] 未找到已运行的 Chrome，启动新实例...")
        return launch_detached_browser()
    
    endpoint = f"http://127.0.0.1:{port}"
    log(f"[..] 连接到现有 Chrome: {endpoint}")
    
    # 等待 Chrome 调试接口可用
    deadline = time.time() + 15
    while time.time() < deadline:
        try:
            import urllib.request
            with urllib.request.urlopen(f"{endpoint}/json/version", timeout=2) as response:
                if response.status == 200:
                    log(f"[OK] Chrome 调试接口已就绪")
                    return None, endpoint
        except Exception:
            time.sleep(1)
    
    raise RuntimeError(f"无法连接到 Chrome 调试端口 {port}")


def connect_over_cdp(playwright, endpoint: str, timeout_seconds: int = 20):
    deadline = time.time() + timeout_seconds
    last_error = None
    while time.time() < deadline:
        try:
            return playwright.chromium.connect_over_cdp(endpoint)
        except Exception as exc:
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"Failed to connect to detached browser at {endpoint}: {last_error}")


def ensure_file(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} does not exist: {path}")


def load_cookies(context) -> None:
    if not COOKIE_FILE.exists():
        log(f"[WARN] Cookie file not found: {COOKIE_FILE}")
        return

    cookies = json.loads(COOKIE_FILE.read_text(encoding="utf-8"))
    if isinstance(cookies, dict):
        cookies = cookies.get("cookies", [])
    if not isinstance(cookies, list):
        raise ValueError("Cookie file format is invalid")
    context.add_cookies(cookies)
    log(f"[OK] Loaded {len(cookies)} cookies")


def save_shot(page, name: str) -> None:
    target = SCREENSHOT_DIR / name
    try:
        page.screenshot(path=str(target), full_page=True, timeout=15_000)
        log(f"[SHOT] {target}")
    except Exception as exc:
        log(f"[WARN] Screenshot skipped: {exc}")


def goto_upload(page) -> None:
    url = "https://creator.douyin.com/creator-micro/content/upload"
    log(f"[..] Open upload page: {url}")
    last_error = None
    for attempt in range(1, 4):
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=90_000)
            time.sleep(3)
            file_input = page.locator('input[type="file"]').first
            title_input = page.locator('input.semi-input-default').first
            if file_input.count() > 0 or title_input.count() > 0 or "creator-micro/content" in page.url:
                return
            file_input.wait_for(state="attached", timeout=20_000)
            return
        except Exception as exc:
            last_error = exc
            log(f"[WARN] Open upload page attempt {attempt} failed: {exc}")
            time.sleep(2)
    raise RuntimeError(f"Failed to open upload page: {last_error}")


def wait_login(page) -> None:
    current = page.url
    if "login" in current or "passport" in current:
        raise RuntimeError("Cookie seems invalid, page redirected to login")
    log(f"[OK] Current page: {current}")


def upload_video(page, video_path: Path) -> None:
    log(f"[..] Upload video: {video_path.name}")
    file_input = page.locator('input[type="file"]').first
    file_input.wait_for(state="attached", timeout=20_000)
    file_input.set_input_files(str(video_path))


def wait_for_edit_form(page, timeout_seconds: int = 180) -> None:
    log("[..] Waiting for edit form")
    title_input = page.locator('input.semi-input-default').first
    editor = page.locator('div[contenteditable="true"]').first
    deadline = time.time() + timeout_seconds

    while time.time() < deadline:
        try:
            if title_input.count() > 0 and title_input.is_visible() and editor.count() > 0 and editor.is_visible():
                log("[OK] Edit form is visible")
                return
        except Exception:
            pass
        time.sleep(2)

    raise TimeoutError("Timed out while waiting for edit form")


def read_page_text(page) -> str:
    try:
        return page.locator("body").inner_text(timeout=3_000)
    except Exception:
        return ""


def is_upload_busy(page) -> tuple[bool, str]:
    body_text = read_page_text(page)
    busy_keywords = [
        "上传中",
        "处理中",
        "转码中",
        "校验中",
        "检测中",
        "封面检测中",
        "发布中",
        "作品还在上传中",
        "等待上传发布完成",
    ]
    for keyword in busy_keywords:
        if keyword in body_text:
            match = re.search(rf"{re.escape(keyword)}[^\r\n]*", body_text)
            return True, (match.group(0).strip() if match else keyword)

    progress_match = re.search(r"((?:上传|处理|转码|校验|检测|发布)[^\r\n]{0,20}?\d{1,3}%)", body_text)
    if progress_match:
        return True, progress_match.group(1).strip()

    busy_selectors = [
        "text=/^上传中$|^处理中$|^转码中$|^校验中$|^发布中$/",
        'button:has-text("取消上传")',
    ]
    for selector in busy_selectors:
        locator = page.locator(selector).first
        try:
            if locator.count() > 0 and locator.is_visible():
                text = locator.inner_text().strip()
                if "点击发布后" in text:
                    continue
                return True, text or selector
        except Exception:
            continue

    disabled_publish = page.locator(
        'button[disabled]:has-text("发布"), button[aria-disabled="true"]:has-text("发布"), '
        'button[disabled]:has-text("提交发布"), button[aria-disabled="true"]:has-text("提交发布")'
    ).first
    try:
        if disabled_publish.count() > 0 and disabled_publish.is_visible():
            return True, "publish button disabled"
    except Exception:
        pass

    return False, ""


def is_form_filled(page, title: str, desc: str) -> bool:
    try:
        title_input = page.locator('input.semi-input-default').first
        current_title = (title_input.input_value() or "").strip()
        editor = page.locator('div[contenteditable="true"]').first
        editor_text = (editor.inner_text() or "").strip()
        return title[:10] in current_title and desc[:10] in editor_text
    except Exception:
        return False


def get_publish_button(page):
    selectors = [
        'button:has-text("发布")',
        'button:has-text("提交发布")',
        'button[type="submit"]',
    ]
    for selector in selectors:
        button = page.locator(selector).last
        try:
            if button.count() == 0:
                continue
            return button
        except Exception:
            continue
    return None


def is_publish_ready(page) -> bool:
    button = get_publish_button(page)
    if button is None:
        return False
    try:
        disabled_attr = button.get_attribute("disabled")
        aria_disabled = button.get_attribute("aria-disabled")
        class_name = (button.get_attribute("class") or "").lower()
        if disabled_attr is None and aria_disabled != "true" and "disabled" not in class_name:
            return True
    except Exception:
        pass
    return False


def wait_for_publish_ready(page, timeout_seconds: int = 900) -> None:
    log("[..] Waiting for publish button to become clickable")
    deadline = time.time() + timeout_seconds
    stable_rounds = 0
    while time.time() < deadline:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        busy, reason = is_upload_busy(page)
        if is_publish_ready(page) and not busy:
            stable_rounds += 1
            log(f"[..] Publish ready check {stable_rounds}/2")
            if stable_rounds >= 2:
                log("[OK] Publish button is clickable")
                return
        else:
            stable_rounds = 0
            state = reason or "publish button not ready"
            log(f"[..] Waiting for publish readiness: {state}")
        time.sleep(3)
    raise TimeoutError("Timed out while waiting for publish button to become clickable")


def wait_for_upload_complete(page, timeout_seconds: int = 600) -> None:
    log("[..] Waiting for upload and processing to finish")
    deadline = time.time() + timeout_seconds
    stable_rounds = 0

    while time.time() < deadline:
        busy, reason = is_upload_busy(page)
        publish_ready = is_publish_ready(page)
        if publish_ready and not busy:
            stable_rounds += 1
            log(f"[..] Upload ready check {stable_rounds}/2")
            if stable_rounds >= 2:
                log("[OK] Upload finished and publish button is ready")
                return
        else:
            stable_rounds = 0
            state = reason or f"publish_ready={publish_ready}"
            log(f"[..] Upload not ready: {state}")

        time.sleep(3)

    raise TimeoutError("Timed out while waiting for upload to complete")


def close_possible_modals(page) -> None:
    for _ in range(3):
        try:
            page.keyboard.press("Escape")
            time.sleep(0.5)
        except Exception:
            pass

        try:
            confirm = page.locator('button:has-text("确认"), button:has-text("确定")').first
            if confirm.count() > 0 and confirm.is_visible():
                confirm.click(force=True)
                time.sleep(0.5)
        except Exception:
            pass


def dismiss_coach_marks(page) -> None:
    selectors = [
        'button:has-text("我知道了")',
        'text=我知道了',
        'button:has-text("知道了")',
    ]
    for _ in range(5):
        clicked = False
        for selector in selectors:
            try:
                locator = page.locator(selector).first
                if locator.count() > 0 and locator.is_visible():
                    locator.click(force=True)
                    clicked = True
                    time.sleep(0.5)
            except Exception:
                continue
        if not clicked:
            return


def fill_title(page, title: str) -> None:
    locator = page.locator('input.semi-input-default').first
    locator.wait_for(state="visible", timeout=20_000)
    locator.scroll_into_view_if_needed()
    locator.click(force=True)
    page.keyboard.press("Control+a")
    locator.fill(title[:30])
    log(f"[OK] Title filled: {title[:30]}")


def fill_desc_and_tags(page, desc: str, tags: list[str]) -> None:
    editor = page.locator('div[contenteditable="true"]').first
    editor.wait_for(state="visible", timeout=20_000)
    editor.scroll_into_view_if_needed()
    editor.click(force=True)
    page.keyboard.press("Control+a")
    page.keyboard.press("Backspace")
    page.keyboard.type(desc, delay=40)
    for tag in tags:
        page.keyboard.type(f" #{tag}", delay=40)
        time.sleep(0.3)
    log(f"[OK] Description and tags filled: {', '.join(tags)}")


def handle_horizontal_cover_prompt(page) -> None:
    try:
        prompt = page.locator('text=/设置横封面获取更多流量|设置横封面/').first
        if prompt.count() == 0 or not prompt.is_visible():
            return

        skip = page.locator('button:has-text("暂不设置")').last
        if skip.count() > 0 and skip.is_visible():
            skip.click(force=True)
            log("[OK] Horizontal cover prompt skipped")
            return

        action = page.locator('button:has-text("设置横封面")').last
        if action.count() > 0 and action.is_visible():
            action.click(force=True)
            log("[WARN] Horizontal cover prompt accepted as fallback")
    except Exception as exc:
        log(f"[WARN] Horizontal cover prompt handling failed: {exc}")


def upload_cover(page, cover_path: Path) -> None:
    if not cover_path.exists():
        log(f"[WARN] Cover not found, skip: {cover_path}")
        return

    try:
        cover_trigger = page.locator('text=/选择封面|上传封面|更换封面/').first
        cover_trigger.wait_for(state="visible", timeout=15_000)
        cover_trigger.click(force=True)

        modal = page.locator("div.dy-creator-content-modal, div.semi-modal-content").last
        modal.wait_for(state="visible", timeout=15_000)

        vertical_tab = modal.locator('text=/设置竖封面|竖封面/').first
        if vertical_tab.count() > 0:
            vertical_tab.click(force=True)
            time.sleep(1)

        uploaded = False
        cover_inputs = modal.locator('input[type="file"]')
        for index in range(cover_inputs.count() - 1, -1, -1):
            try:
                current = cover_inputs.nth(index)
                if not current.is_enabled():
                    continue
                current.set_input_files(str(cover_path))
                log(f"[OK] Cover uploaded: {cover_path.name}")
                uploaded = True
                break
            except Exception:
                continue

        time.sleep(3)

        if not uploaded:
            try:
                thumbnails = modal.locator("canvas, img")
                if thumbnails.count() > 0:
                    thumbnails.first.click(force=True)
                    log("[WARN] Custom cover input unavailable, fallback to selected frame")
                    time.sleep(1)
            except Exception:
                pass

        set_vertical = modal.locator('button:has-text("设置竖封面")').last
        if set_vertical.count() > 0 and set_vertical.is_enabled():
            set_vertical.click(force=True)
            time.sleep(1)

        complete = modal.locator('button:has-text("完成")').last
        complete.wait_for(state="visible", timeout=15_000)
        for _ in range(10):
            try:
                disabled_attr = complete.get_attribute("disabled")
                aria_disabled = complete.get_attribute("aria-disabled")
                class_name = (complete.get_attribute("class") or "").lower()
                if disabled_attr is None and aria_disabled != "true" and "disabled" not in class_name:
                    break
            except Exception:
                pass
            time.sleep(1)
        complete.click(force=True)
        handle_horizontal_cover_prompt(page)
        modal.wait_for(state="hidden", timeout=20_000)
        log("[OK] Cover modal completed")
    except Exception as exc:
        log(f"[WARN] Cover upload skipped: {exc}")


def click_publish(page) -> None:
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)
    button = get_publish_button(page)
    if button is None:
        raise RuntimeError("Publish button not found")
    button.scroll_into_view_if_needed()
    button.click(force=True)
    log("[OK] Publish button clicked")


def click_publish_early(page, retries: int = 3) -> None:
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            click_publish(page)
            return
        except Exception as exc:
            last_error = exc
            log(f"[WARN] Early publish click attempt {attempt} failed: {exc}")
            time.sleep(2)
    raise RuntimeError(f"Early publish click failed: {last_error}")


def confirm_publish_click(page, timeout_seconds: int = 20) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        body_text = read_page_text(page)
        if "上传中，请勿关闭页面" in body_text or "等待上传发布完成" in body_text or "发布中" in body_text:
            log("[OK] Publish click acknowledged by page state")
            return

        button = get_publish_button(page)
        try:
            if button is not None and button.count() > 0:
                button_text = (button.inner_text() or "").strip()
                disabled_attr = button.get_attribute("disabled")
                aria_disabled = button.get_attribute("aria-disabled")
                if button_text not in {"发布", "提交发布"} or disabled_attr is not None or aria_disabled == "true":
                    log("[OK] Publish click acknowledged by button state")
                    return
        except Exception:
            pass

        time.sleep(1)

    raise TimeoutError("Publish button click was not acknowledged by the page")


def handle_auto_video_cover(page) -> bool:
    try:
        tip = page.get_by_text("请设置封面后再发布").first
        if tip.count() == 0 or not tip.is_visible():
            return False
        log("[..] Publish blocked by cover validation")

        recommend = page.locator('[class^="recommendCover-"]').first
        if recommend.count() == 0:
            return False

        recommend.click(force=True)
        time.sleep(1)

        confirm = page.get_by_role("button", name="确定").last
        if confirm.count() > 0 and confirm.is_visible():
            confirm.click(force=True)
            time.sleep(1)

        complete = page.locator('button:has-text("完成")').last
        if complete.count() > 0 and complete.is_visible():
            complete.click(force=True)
            time.sleep(1)

        log("[OK] Recommended cover selected")
        return True
    except Exception as exc:
        log(f"[WARN] Auto cover fallback failed: {exc}")
        return False


def resume_unfinished_draft(page) -> bool:
    selectors = [
        'text=继续编辑',
        'button:has-text("继续编辑")',
        'a:has-text("继续编辑")',
    ]
    for selector in selectors:
        try:
            locator = page.locator(selector).first
            if locator.count() > 0 and locator.is_visible():
                locator.click(force=True)
                log("[WARN] Returned to unfinished draft page, resuming editor")
                time.sleep(2)
                return True
        except Exception:
            continue
    return False


def wait_for_publish_success(page, timeout_seconds: int = 90) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        current_url = page.url
        if "content/manage" in current_url:
            log(f"[OK] Publish success: {current_url}")
            return

        success_text = page.locator('text=/发布成功|已发布|上传成功|投稿成功/')
        try:
            if "content/post/video" not in current_url and success_text.count() > 0:
                log(f"[OK] Publish success by page text: {current_url}")
                return
        except Exception:
            pass

        try:
            publish_button = get_publish_button(page)
            if (
                "content/post/video" in current_url
                and publish_button is not None
                and publish_button.count() > 0
                and publish_button.is_visible()
            ):
                button_text = (publish_button.inner_text() or "").strip()
                if button_text in {"发布", "提交发布"}:
                    log("[..] Still on editor page after publish click, waiting for actual success")
        except Exception:
            pass

        if resume_unfinished_draft(page):
            wait_for_publish_ready(page, timeout_seconds=180)
            click_publish(page)
            continue

        if handle_auto_video_cover(page):
            click_publish(page)

        time.sleep(2)

    raise TimeoutError(f"Publish status not confirmed, current url: {page.url}")


def main() -> int:
    args = build_parser().parse_args()
    video_path = Path(args.video)
    cover_path = Path(args.cover)

    ensure_file(video_path, "Video")

    log("=" * 60)
    log("Douyin uploader debug")
    log("=" * 60)
    log(f"Video : {video_path}")
    log(f"Title : {args.title}")
    log(f"Desc  : {args.desc}")
    log(f"Tags  : {', '.join(args.tags)}")
    log(f"Cover : {cover_path if cover_path.exists() else 'skip'}")
    log(f"Mode  : {'publish' if args.publish else 'fill-only'}")
    log("")

    with sync_playwright() as playwright:
        browser = None
        detached_browser = False
        endpoint = None
        
        # 优先连接到用户已登录的 Chrome
        if args.use_existing_chrome or not args.close_browser:
            process, endpoint = connect_to_existing_chrome(playwright, args.debug_port)
            if endpoint:
                log("[OK] 使用现有 Chrome 浏览器（已登录状态）")
                browser = connect_over_cdp(playwright, endpoint)
                detached_browser = True
                context = browser.contexts[0] if browser.contexts else browser.new_context()
                page = context.pages[0] if context.pages else context.new_page()
            else:
                # 没有现有 Chrome，启动新的
                log("[..] 启动新的 Chrome 实例...")
                _, endpoint = launch_detached_browser()
                browser = connect_over_cdp(playwright, endpoint)
                detached_browser = True
                context = browser.contexts[0] if browser.contexts else browser.new_context()
                page = context.pages[0] if context.pages else context.new_page()
        elif args.close_browser:
            browser = playwright.chromium.launch(
                headless=args.headless,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-gpu",
                    "--no-sandbox",
                ],
            )
            context = browser.new_context(
                viewport={"width": 1600, "height": 1200},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/134.0.0.0 Safari/537.36"
                ),
                geolocation={"latitude": 31.2304, "longitude": 121.4737},
            )
            page = context.new_page()
        else:
            _, endpoint = launch_detached_browser()
            browser = connect_over_cdp(playwright, endpoint)
            detached_browser = True
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            page = context.pages[0] if context.pages else context.new_page()

        context.grant_permissions(["geolocation"], origin="https://creator.douyin.com")
        page.set_default_timeout(20_000)
        exit_code = 0

        try:
            load_cookies(context)
            goto_upload(page)
            wait_login(page)
            dismiss_coach_marks(page)
            save_shot(page, "01_upload_page.png")

            upload_video(page, video_path)
            wait_for_edit_form(page)
            close_possible_modals(page)
            dismiss_coach_marks(page)
            fill_title(page, args.title)
            fill_desc_and_tags(page, args.desc, args.tags)
            upload_cover(page, cover_path)
            save_shot(page, "02_form_filled_while_uploading.png")

            if not is_form_filled(page, args.title, args.desc):
                log("[WARN] Form content not detected after fill attempt, retry once")
                fill_title(page, args.title)
                fill_desc_and_tags(page, args.desc, args.tags)

            if args.publish:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
                close_possible_modals(page)
                dismiss_coach_marks(page)
                save_shot(page, "02_after_video_upload.png")
                save_shot(page, "03_form_filled.png")
                click_publish_early(page)
                confirm_publish_click(page)
                save_shot(page, "04_after_publish_click.png")
            else:
                page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                time.sleep(1)
                wait_for_publish_ready(page, timeout_seconds=args.publish_wait_seconds)
                close_possible_modals(page)
                dismiss_coach_marks(page)
                save_shot(page, "02_after_video_upload.png")
                save_shot(page, "03_form_filled.png")
                log("[INFO] Form is ready. Re-run with --publish to submit.")

            if args.close_browser:
                time.sleep(5)
            else:
                log("[INFO] Publish click confirmed. Browser stays open after script exit.")
        except (PlaywrightTimeoutError, TimeoutError, FileNotFoundError, RuntimeError, ValueError) as exc:
            log(f"[ERR] {exc}")
            try:
                save_shot(page, "debug_error.png")
            except Exception:
                pass
            exit_code = 1
        finally:
            if args.close_browser and browser is not None:
                browser.close()
            elif detached_browser and browser is not None:
                try:
                    browser.close()
                except Exception:
                    pass

        return exit_code


if __name__ == "__main__":
    sys.exit(main())
