# 🎵 TikTok Skill 使用指南

**测试视频**: `storage/videos/test.mp4` (14.95 MB) ✅

---

## 🚀 快速开始

### 第 1 步：配置 Rube MCP

在你的 AI 客户端中添加 MCP 服务器。

#### Claude Code 配置

编辑配置文件（通常在 `~/.config/claude-code/config.json`）：

```json
{
  "mcpServers": {
    "rube": {
      "url": "https://rube.app/mcp"
    }
  }
}
```

#### Cursor 配置

1. 打开设置
2. 找到 MCP Servers
3. 添加新服务器：
   - Name: `rube`
   - URL: `https://rube.app/mcp`

#### 其他客户端

参考各客户端的 MCP 配置文档。

---

### 第 2 步：连接 TikTok 账号

启动 AI 客户端后，输入：

```
帮我连接 TikTok 账号
```

AI 会返回一个授权链接：

```
请点击以下链接授权 TikTok 连接：
https://composio.dev/authorize?code=xxxxx
```

**操作步骤**：
1. 复制链接到浏览器
2. 登录 TikTok 账号
3. 点击"授权"
4. 返回 AI 客户端

---

### 第 3 步：上传视频

连接成功后，输入：

```
帮我上传这个视频到 TikTok：./storage/videos/test.mp4

标题："AI 自动化测试视频 #AI #自动化 #科技"
隐私级别：公开
允许合拍：是
允许拼接：是
允许评论：是
```

**AI 会自动执行**：

1. ✅ 调用 `TIKTOK_UPLOAD_VIDEO` 上传视频
2. ✅ 调用 `TIKTOK_FETCH_PUBLISH_STATUS` 检查状态
3. ✅ 调用 `TIKTOK_PUBLISH_VIDEO` 发布视频

---

### 第 4 步：查看结果

上传完成后，可以查看：

#### 查看发布状态

```
帮我检查刚才发布的视频状态
```

#### 查看视频列表

```
帮我查看我发布的视频列表
```

#### 查看账号数据

```
帮我查看我的 TikTok 账号数据
```

---

## 📝 完整测试脚本

### 测试 1：检查连接状态

```
检查我的 TikTok 连接状态
```

**预期响应**：
```
您的 TikTok 连接状态：ACTIVE
已授权范围：video.upload, video.publish, user.info
```

---

### 测试 2：上传视频

```
帮我上传视频到 TikTok

文件路径：./storage/videos/test.mp4
标题：AI 自动化测试视频 #AI #自动化 #科技
隐私级别：PUBLIC_TO_EVERYONE
```

**预期流程**：
```
📹 正在上传视频...
✅ 上传成功，publish_id: xxxxx

⏳ 正在处理视频...
✅ 处理完成

📤 正在发布视频...
✅ 发布成功！

视频链接：https://www.tiktok.com/@yourname/video/xxxxx
```

---

### 测试 3：查看视频

```
帮我查看我发布的视频
```

**预期响应**：
```
您发布的视频：

1. AI 自动化测试视频
   - 发布时间：2026-03-16 17:10
   - 播放量：123
   - 点赞：45
   - 链接：https://...

2. 之前的视频
   ...
```

---

### 测试 4：查看统计数据

```
帮我看看我的 TikTok 账号数据
```

**预期响应**：
```
您的 TikTok 账号数据：

👥 粉丝：1,234
👤 关注：567
📹 视频：89
❤️ 获赞：12,345
```

---

## ⚙️ 工具参考

### 核心工具

| 工具 | 功能 | 使用场景 |
|------|------|----------|
| `TIKTOK_UPLOAD_VIDEO` | 上传单个视频 | 发布新视频 |
| `TIKTOK_PUBLISH_VIDEO` | 发布已上传视频 | 完成发布 |
| `TIKTOK_FETCH_PUBLISH_STATUS` | 检查发布状态 | 等待处理 |
| `TIKTOK_LIST_VIDEOS` | 列出视频 | 查看作品 |
| `TIKTOK_GET_USER_PROFILE` | 获取个人资料 | 查看信息 |
| `TIKTOK_GET_USER_STATS` | 获取统计数据 | 查看数据 |

---

## ⚠️ 注意事项

### 视频要求

- ✅ 格式：MP4 或 WebM
- ✅ 大小：≤ 4GB（测试视频 14.95 MB ✅）
- ✅ 时长：≤ 10 分钟
- ✅ 分辨率：720p 及以上

### 标题要求

- 字符数限制（因地区而异）
- 可以包含话题标签（#）
- 可以@其他用户

### 隐私级别

| 级别 | 说明 |
|------|------|
| `PUBLIC_TO_EVERYONE` | 公开（所有人可见） |
| `MUTUAL_FOLLOW_FRIENDS` | 互相关注的朋友 |
| `FOLLOWER_OF_CREATOR` | 仅粉丝可见 |
| `SELF_ONLY` | 仅自己可见 |

### 发布流程

**重要**：上传和发布是两个步骤！

```
1. 上传视频 (30-120 秒)
   ↓
2. 等待处理完成
   ↓
3. 发布视频
```

---

## 🔧 故障排除

### 问题 1：找不到 Rube MCP

**解决**：
```
检查 MCP 服务器配置
添加 https://rube.app/mcp
重启 AI 客户端
```

### 问题 2：TikTok 未连接

**解决**：
```
帮我连接 TikTok 账号
```

### 问题 3：上传失败

**可能原因**：
- 视频格式不支持
- 文件太大
- 网络连接问题

**解决**：
```
检查视频文件格式
确保文件大小 < 4GB
检查网络连接
```

### 问题 4：发布失败

**可能原因**：
- 视频还在处理中
- Token 过期
- 权限不足

**解决**：
```
等待 30 秒后重试
重新连接 TikTok 账号
检查授权范围
```

---

## 💡 使用技巧

### 技巧 1：批量上传

```
帮我上传以下视频到 TikTok：
1. ./video1.mp4 - "视频 1 #话题"
2. ./video2.mp4 - "视频 2 #话题"
3. ./video3.mp4 - "视频 3 #话题"
```

### 技巧 2：定时发布

```
帮我安排发布视频：
视频：./video.mp4
标题："新视频"
发布时间：今天晚上 8 点
```

### 技巧 3：使用热门话题

```
帮我发布视频，添加这些话题：
#AI #自动化 #科技 #短视频 #热门
```

---

## 📊 测试清单

- [ ] 配置 Rube MCP
- [ ] 连接 TikTok 账号
- [ ] 检查连接状态
- [ ] 上传测试视频
- [ ] 等待处理完成
- [ ] 发布视频
- [ ] 查看发布结果
- [ ] 查看视频列表
- [ ] 查看账号数据

---

## 🎯 快速命令参考

```bash
# 检查连接
检查我的 TikTok 连接状态

# 连接账号
帮我连接 TikTok 账号

# 上传视频
帮我上传这个视频到 TikTok: ./storage/videos/test.mp4

# 发布视频
帮我发布视频，标题："AI 测试 #科技"

# 查看视频
帮我查看我发布的视频

# 查看数据
帮我查看我的 TikTok 账号数据

# 检查状态
帮我检查刚才发布的视频状态
```

---

## 🔗 相关资源

- **Rube MCP**: https://rube.app/
- **Composio**: https://composio.dev/
- **TikTok API**: https://developers.tiktok.com/
- **技能源码**: https://github.com/sickn33/antigravity-awesome-skills

---

**准备就绪！现在可以在 AI 客户端中使用 TikTok Skill 了！** 🎉

**测试视频已准备**：`storage/videos/test.mp4` (14.95 MB)
