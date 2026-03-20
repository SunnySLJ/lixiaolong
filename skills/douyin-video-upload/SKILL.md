---
name: douyin-video-upload
description: Upload and publish a video to Douyin Creator Center with Playwright using local cookies, title, description, tags, and optional cover image. Use when the user wants to upload/publish a Douyin video, debug the Douyin creator upload flow, keep the browser open after clicking publish, or rerun the local Douyin uploader script.
---

# Douyin Video Upload

Use this skill when the user wants to upload a video to Douyin from this workspace.

## Trigger cases

- "上传抖音视频"
- "继续上传抖音"
- "调试抖音发布脚本"
- "点发布但浏览器别关"
- "用 cookies 自动发布抖音"

## Workflow

1. Confirm the source files exist:
   - video
   - optional cover
   - `douyin_cookies.json`
2. Use the bundled launcher in `scripts/run-upload.ps1`.
3. For publish mode, prefer `--publish`.
4. Do not pass `--close-browser` unless the user explicitly asks to auto-close the browser.
5. Treat "publish click acknowledged" as success for the automation step when the user wants the browser to remain open and let Douyin continue processing by itself.

## Commands

- Fill only:
  `powershell -ExecutionPolicy Bypass -File .\douyin-video-upload\scripts\run-upload.ps1`
- Publish and keep browser open:
  `powershell -ExecutionPolicy Bypass -File .\douyin-video-upload\scripts\run-upload.ps1 -Publish`
- Override files:
  `powershell -ExecutionPolicy Bypass -File .\douyin-video-upload\scripts\run-upload.ps1 -Video "C:\path\video.mp4" -Cover "C:\path\cover.jpg" -Title "标题" -Desc "描述"`

## Notes

- The actual automation lives in `scripts/douyin_upload.py`.
- The script uses the local cookie file `douyin_cookies.json`.
- In publish mode without `--close-browser`, the launcher relies on the uploader's detached-browser behavior so the script can exit while the browser stays open.
- If publishing appears unsuccessful, inspect `04_after_publish_click.png` and `debug_error.png`.
