# 🎬 准备测试视频

## 步骤 1：准备视频文件

请准备一个测试视频文件（MP4 格式），要求：
- 时长：10-60 秒
- 大小：< 100MB
- 格式：MP4
- 分辨率：720p 或 1080p

可以将视频放在：`storage/videos/` 目录

## 步骤 2：登录抖音

```bash
cd C:\Users\爽爽\.openclaw\workspace\douyin-auto-publish
python scripts/login.py
```

运行后会：
1. 自动打开浏览器
2. 显示抖音登录二维码
3. 使用抖音 APP 扫码登录
4. 登录成功后自动保存 Cookie

## 步骤 3：发布视频

登录成功后，运行：

```bash
python scripts/publish.py \
  --video ./storage/videos/你的视频.mp4 \
  --title "测试视频标题" \
  --desc "这是一个测试视频 #测试 #抖音发布工具"
```

## 快速测试命令

如果已经有视频文件，可以直接运行：

```bash
# 1. 登录
python scripts/login.py

# 2. 发布（替换为你的视频路径）
python scripts/publish.py -v ./storage/videos/test.mp4 -t "我的测试视频" -d "#测试 #AI 自动化"
```

## 注意事项

1. **视频内容**: 建议使用简单的测试视频，不要使用有版权的内容
2. **发布频率**: 测试期间不要频繁发布，避免触发风控
3. **账号安全**: 使用小号测试，不要使用主账号

---

**准备好了吗？请提供一个测试视频文件，然后我们开始！** 🎉
