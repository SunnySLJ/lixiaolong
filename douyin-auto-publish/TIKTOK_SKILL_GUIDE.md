# 🎵 TikTok Automation Skill 使用说明

**技能名称**: tiktok-automation  
**安装时间**: 2026-03-16  
**风险等级**: ⚠️ Medium Risk  
**来源**: Community (sickn33/antigravity-awesome-skills)

---

## ✅ 安装状态

- ✅ 已安装到 OpenClaw
- ✅ 已安装到 Claude Code
- ✅ 已安装到 Codex、Cursor 等 42 个平台
- ⚠️ 需要配置 Rube MCP 连接

---

## 🔧 功能特性

### 核心功能

1. **📹 视频上传和发布**
   - 上传单个视频
   - 上传多个视频
   - 发布已上传的视频
   - 设置隐私级别

2. **📸 照片发布**
   - 发布照片到 TikTok
   - 设置标题和隐私

3. **📊 视频管理**
   - 列出已发布的视频
   - 查看视频详情
   - 分页浏览

4. **👤 用户资料**
   - 查看个人资料
   - 查看统计数据（粉丝、点赞等）
   - 查看基本信息

5. **🔍 状态检查**
   - 检查上传状态
   - 检查发布状态
   - 检查处理进度

---

## 🚀 使用前准备

### 1. 连接 Rube MCP

**添加 MCP 服务器**：

在 Claude/Codex 等客户端配置中添加：
```json
{
  "mcpServers": {
    "rube": {
      "url": "https://rube.app/mcp"
    }
  }
}
```

**无需 API Key**，只需添加端点即可使用。

### 2. 连接 TikTok 账号

**步骤**：

1. 调用 `RUBE_MANAGE_CONNECTIONS` with toolkit `tiktok`
2. 如果连接未激活，会返回授权链接
3. 点击链接完成 TikTok OAuth 授权
4. 确认连接状态为 `ACTIVE`

---

## 📝 使用示例

### 示例 1：上传并发布视频

**当你想让 AI 帮你发布视频到 TikTok 时**：

```
帮我上传并发布这个视频到 TikTok：
- 视频文件：./my_video.mp4
- 标题："我的新视频 #AI #自动化"
- 隐私：公开
```

**AI 会执行的操作**：

1. `TIKTOK_UPLOAD_VIDEO` - 上传视频
2. `TIKTOK_FETCH_PUBLISH_STATUS` - 检查处理状态
3. `TIKTOK_PUBLISH_VIDEO` - 发布视频

**发布参数**：
- `title`: 视频标题
- `privacy_level`: "PUBLIC_TO_EVERYONE"
- `disable_duet`: false
- `disable_stitch`: false
- `disable_comment`: false

---

### 示例 2：发布照片

```
帮我发一张照片到 TikTok：
- 照片：./photo.jpg
- 标题："美好的一天 #日常"
```

---

### 示例 3：查看我的视频

```
帮我查看我发布的视频列表
```

会返回：
- 视频 ID
- 标题
- 创建时间
- 分享链接
- 时长

---

### 示例 4：查看账号数据

```
帮我看看我的 TikTok 账号数据
```

会返回：
- 粉丝数
- 关注数
- 视频数
- 获赞数

---

## ⚙️ 核心工具

### 视频相关

| 工具 | 功能 | 参数 |
|------|------|------|
| `TIKTOK_UPLOAD_VIDEO` | 上传单个视频 | video, title |
| `TIKTOK_UPLOAD_VIDEOS` | 上传多个视频 | videos |
| `TIKTOK_PUBLISH_VIDEO` | 发布视频 | publish_id, title, privacy_level |
| `TIKTOK_FETCH_PUBLISH_STATUS` | 检查发布状态 | publish_id |

### 照片相关

| 工具 | 功能 | 参数 |
|------|------|------|
| `TIKTOK_POST_PHOTO` | 发布照片 | photo, title, privacy_level |

### 管理相关

| 工具 | 功能 | 参数 |
|------|------|------|
| `TIKTOK_LIST_VIDEOS` | 列出视频 | max_count, cursor |
| `TIKTOK_GET_USER_PROFILE` | 获取个人资料 | (无) |
| `TIKTOK_GET_USER_STATS` | 获取统计数据 | (无) |
| `TIKTOK_GET_USER_BASIC_INFO` | 获取基本信息 | (无) |

---

## ⚠️ 注意事项

### 视频要求

- **格式**: MP4 或 WebM
- **大小**: 最大 4GB
- **时长**: 最多 10 分钟
- **分辨率**: 建议 720p 及以上

### 照片要求

- **格式**: JPEG、PNG、WebP
- **大小**: 遵循 TikTok 最新指南

### 标题限制

- 字符数有限制（因地区而异）
- 可以包含话题标签（#）
- 可以@其他用户

### 隐私级别

可用选项（区分大小写）：
- `PUBLIC_TO_EVERYONE` - 公开
- `MUTUAL_FOLLOW_FRIENDS` - 互相关注的朋友
- `FOLLOWER_OF_CREATOR` - 仅粉丝可见
- `SELF_ONLY` - 仅自己可见

### 发布流程

**重要**：上传和发布是**两个独立步骤**！

```
1. 上传视频 → 获取 publish_id
2. 等待处理完成（轮询状态）
3. 发布视频
```

处理时间通常需要 30-120 秒。

---

## 🔒 安全提示

### 权限说明

- 技能需要 TikTok OAuth 授权
- 授权范围包括：video.upload, video.publish
- Token 会过期，需要定期重新授权

### 速率限制

- TikTok API 有严格的速率限制
- 上传操作有每日限制
- 遇到 429 错误时使用指数退避

### 内容合规

- 视频必须符合 TikTok 社区准则
- 不要上传侵权内容
- 不要使用违规音乐或素材

---

## 🆚 与抖音发布工具对比

| 特性 | TikTok Skill | 抖音发布工具 |
|------|-------------|-------------|
| 平台 | TikTok (国际版) | 抖音 (中国版) |
| 实现方式 | Rube MCP (Composio) | 官方 API / 网页自动化 |
| 需要资质 | 无 | 官方 API 需要企业 |
| 支持内容 | 视频 + 照片 | 视频 |
| 数据查看 | ✅ | ✅ (官方 API) |
| 批量发布 | ⚠️ | ✅ (开发中) |

---

## 💡 使用技巧

### 1. 先检查连接

使用前确保 TikTok 连接已激活：
```
检查我的 TikTok 连接状态
```

### 2. 分批上传

如果要发布多个视频，建议分批上传，避免触发速率限制。

### 3. 监控状态

发布后检查状态：
```
帮我检查刚才发布的视频状态
```

### 4. 使用话题标签

标题中添加热门话题可以提高曝光：
```
#AI #自动化 #科技 #短视频
```

---

## 🎯 快速开始

### 第一步：配置 Rube MCP

在你的 AI 客户端添加 MCP 服务器：
```
https://rube.app/mcp
```

### 第二步：连接 TikTok

告诉 AI：
```
帮我连接 TikTok 账号
```

### 第三步：发布视频

告诉 AI：
```
帮我发布这个视频到 TikTok：./video.mp4
标题："我的第一个 TikTok 视频"
```

---

## 📚 相关资源

- **Rube MCP**: https://rube.app/
- **Composio**: https://composio.dev/
- **TikTok API 文档**: https://developers.tiktok.com/
- **技能源码**: https://github.com/sickn33/antigravity-awesome-skills

---

**安装完成！现在可以开始使用 TikTok 自动化功能了！** 🎉
