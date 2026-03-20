---
name: douyin-video-upload
description: Upload videos to Douyin (TikTok China) using the user's logged-in Chrome browser session. Use when the user wants to publish videos to their Douyin account with custom title, description, and tags. Requires the user to be logged into Douyin Creator Center in Chrome.
---

# Douyin Video Upload Skill

使用用户已登录的 Chrome 浏览器会话上传视频到抖音创作者中心。

## 前置条件

1. 用户已在 Chrome 浏览器中登录抖音创作者中心 (https://creator.douyin.com)
2. Chrome 浏览器开启了远程调试端口（通常为 18800）
3. 视频文件已存在于本地

## 输入参数

- **video_path**: 视频文件路径（必填）
- **title**: 视频标题（必填，最多 30 字）
- **description**: 视频描述（必填，可包含话题标签）
- **tags**: 话题标签列表（可选，如 ["日常", "vlog", "生活记录"]）
- **cover_path**: 封面图片路径（可选，不传则使用 AI 智能封面）
- **publish**: 是否自动点击发布（可选，默认 true）
- **debug_port**: Chrome 远程调试端口（可选，默认 18800）

## 工作流程

1. **连接 Chrome**: 通过 CDP 连接到用户已登录的 Chrome 会话
2. **打开上传页面**: 导航到抖音创作者中心上传页面
3. **上传视频**: 选择并上传视频文件
4. **等待 AI 封面生成**: 等待抖音 AI 自动生成封面（约 10-20 秒）
5. **选择封面**: 点击"选择封面"，等待 AI 封面生成完成后点击"完成"
6. **填写信息**: 输入标题、描述和话题标签
7. **点击发布**: 关闭可能的弹窗，点击发布按钮
8. **等待审核**: 浏览器保持打开，视频进入审核状态

## 执行示例

```bash
python scripts/douyin_upload.py \
  --video "/path/to/video.mp4" \
  --title "平凡日子里的小确幸 ✨" \
  --desc "记录生活中的美好瞬间 #日常 #vlog" \
  --tags 日常 vlog 生活记录 治愈 \
  --publish \
  --debug-port 18800
```

## 注意事项

1. **封面必须设置**: 抖音要求必须设置封面，如果不传 cover_path 则使用 AI 智能生成的封面
2. **等待 AI 封面**: AI 封面生成需要 10-20 秒，必须等待生成完成后再继续
3. **处理弹窗**: 发布时可能会遇到"设置横封面"等弹窗，需要关闭后再点发布
4. **浏览器保持打开**: 发布后浏览器保持打开状态，视频进入审核流程
5. **审核时间**: 视频审核通常需要几分钟到几小时不等

## 错误处理

- 如果找不到 Chrome 调试端口，提示用户启动带远程调试的 Chrome
- 如果 AI 封面生成超时，尝试手动选择一个封面
- 如果发布按钮不可点击，检查是否有弹窗未关闭
- 如果上传失败，保存截图并返回错误信息

## 输出

- 成功：返回"发布成功，视频正在审核中"
- 失败：返回具体错误原因和截图路径

## 依赖

- Python 3.9+
- Playwright
- 已登录抖音的 Chrome 浏览器
