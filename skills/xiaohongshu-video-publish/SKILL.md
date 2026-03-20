---
name: xiaohongshu-video-publish
description: 小红书视频自动发布技能。使用 OpenClaw 内置浏览器上传视频到小红书创作平台，自动填写标题、话题并完成发布。
---

# 小红书视频发布技能

## 触发条件
- "发布视频到小红书"
- "上传视频到小红书"
- "帮我发小红书视频"
- "小红书视频发布"
- 用户提供视频路径并要求发布到小红书

## 前置要求
1. 用户已登录小红书创作平台 (creator.xiaohongshu.com)
2. 视频文件存在于本地路径
3. 浏览器工具可用 (profile="user")

## 执行流程

### 1. 环境检查
```
- 检查浏览器状态：browser action=status
- 获取标签页列表：browser action=tabs
- 查找小红书创作中心标签页 (creator.xiaohongshu.com)
- 如无则打开：browser action=open url=https://creator.xiaohongshu.com/
```

### 2. 进入视频发布页面
```
- 切换到小红书标签页：browser action=focus targetId=<id>
- 导航到发布页：browser action=navigate url=https://creator.xiaohongshu.com/publish/publish
- 等待页面加载：browser action=wait timeMs=3000
```

### 3. 上传视频文件
```
- 准备视频文件：复制到 /tmp/openclaw/uploads/ 目录
- 截图确认页面状态：browser action=snapshot
- 上传视频：browser action=upload inputRef=<文件选择器 ref> paths=[<视频路径>]
- 等待上传处理：browser action=wait timeMs=15000
```

### 4. 填写标题和描述
```
- 截图确认编辑页面：browser action=snapshot
- 填写标题：browser action=type ref=<标题输入框 ref> text=<标题>
- 填写话题：browser action=type ref=<描述框 ref> text=<话题标签>
- 等待输入生效：browser action=wait timeMs=1000
```

### 5. 发布视频
```
- 截图确认发布按钮可见：browser action=snapshot
- 点击发布：browser action=click ref=<发布按钮 ref>
- 等待发布处理：browser action=wait timeMs=8000
- 检查发布结果：browser action=snapshot
```

### 6. 结果确认
```
- 如返回上传页 = 发布成功
- 如仍在编辑页 = 可能需要手动确认
- 导航到笔记管理页确认：url=https://creator.xiaohongshu.com/note/manage
```

## 关键选择器 (动态获取)

| 元素 | 选择方式 | 说明 |
|------|----------|------|
| 文件选择器 | `button "选择文件"` | 上传视频入口 |
| 标题输入框 | `textbox "填写标题会有更多赞哦"` | 标题输入 |
| 描述输入框 | `textbox` (第二个) | 正文和话题 |
| 发布按钮 | `button "发布"` | 底部发布按钮 |

## 内容规范

### 标题
- 长度：≤20 字最佳
- 格式：`主题｜副标题` 或 `情绪词 + 具体对象`
- 示例：`春日随拍小片段｜城市日常记录`

### 话题标签
- 数量：3-5 个
- 格式：`#话题 1 #话题 2 #话题 3`
- 推荐：`#生活美学 #日常文案 #我的生活碎片`

## 错误处理

### 浏览器超时
```
- 重启网关：gateway action=restart
- 重新打开小红书：browser action=open
- 重试上传流程
```

### 页面不存在
```
- 检查 URL 是否正确
- 尝试首页：https://creator.xiaohongshu.com/new/home
- 从首页点击"发布视频笔记"
```

### 上传失败
```
- 检查视频格式 (mp4/mov)
- 检查文件大小 (≤20GB)
- 检查文件路径是否正确
- 重新复制文件到 uploads 目录
```

### 发布按钮点击无效
```
- 刷新页面快照：browser action=snapshot
- 重新获取元素 ref
- 重试点击
- 如仍失败，提示用户手动点击
```

## 输出格式

发布成功后输出：
```
✅ 小红书视频发布完成！

📹 视频：<文件名>
📝 标题：<标题>
🏷️ 话题：<话题列表>
🔗 查看：https://www.xiaohongsh.com/
```

## 注意事项

1. **浏览器 profile**：使用 `profile="user"` 连接用户已登录的浏览器
2. **文件路径**：必须先复制到 `/tmp/openclaw/uploads/` 目录
3. **等待时间**：视频上传和处理需要时间，适当增加 wait 时间
4. **页面快照**：关键步骤前截图，便于调试和确认
5. **发布确认**：小红书发布后通常会返回上传页，这是正常现象

## 示例命令

```bash
# 发布视频
browser action=open url=https://creator.xiaohongshu.com/publish/publish
browser action=upload inputRef=5_19 paths=["C:\\path\\to\\video.mp4"]
browser action=type ref=6_9 text="视频标题"
browser action=type ref=6_11 text="#话题 1 #话题 2"
browser action=click ref=6_74
```

## 相关技能

- xiaohongshu-ops: 小红书全链路运营（包含发布、回复、分析）
- nano-banana-pro: 封面图生成

---

**版本：** 1.0  
**最后更新：** 2026-03-19  
**测试状态：** ✅ 已验证 (2026-03-19)
