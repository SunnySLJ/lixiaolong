# 小红书视频一键发布技能

🤖 使用 OpenClaw 内置浏览器自动上传视频到小红书创作平台

## ✨ 特性

- 🚀 **一键发布** - 一条命令完成视频上传、填写标题、添加话题、发布
- 🔧 **自动恢复** - 浏览器超时自动重启网关和浏览器
- 📋 **内容规范** - 自动检查标题长度、话题格式
- 🎯 **错误处理** - 详细的错误提示和恢复建议
- 📊 **发布确认** - 自动验证发布状态

---

## 📋 前置要求

### 必需环境

| 项目 | 版本 | 说明 |
|------|------|------|
| **Node.js** | >=18.0.0 | [下载地址](https://nodejs.org/) |
| **OpenClaw** | >=2026.3.0 | [安装指南](https://docs.openclaw.ai) |
| **浏览器** | Chromium/Chrome | OpenClaw 自动管理 |
| **小红书账号** | - | 已登录创作后台 |

### 检查清单

```bash
# 1. 检查 Node.js
node --version  # 应 >= v18.0.0

# 2. 检查 OpenClaw
openclaw status  # 应显示运行状态

# 3. 检查小红书登录
# 手动访问：https://creator.xiaohongshu.com/
# 确认能看到你的账号名
```

---

## 🚀 安装

### 方式 1：通过 ClawHub（推荐）

```bash
# 安装技能
clawhub install xiaohongshu-video-publish

# 验证安装
openclaw skills list
```

### 方式 2：手动安装

```bash
# 1. 克隆或复制技能到 workspace
cd C:\Users\爽爽\.openclaw\workspace\skills

# 2. 安装依赖
cd xiaohongshu-video-publish
npm install

# 3. 验证安装
node scripts/check-env.js
```

### 方式 3：从现有目录使用

技能已在 `C:\Users\爽爽\.openclaw\workspace\skills\xiaohongshu-video-publish`

```bash
cd C:\Users\爽爽\.openclaw\workspace\skills\xiaohongshu-video-publish
npm install
```

---

## 📖 使用方法

### 快速开始

```bash
# 基础发布
node scripts/publish.js --video="C:\Users\爽爽\Desktop\视频.mp4" --title="春日随拍"

# 带自定义话题
node scripts/publish.js --video="视频.mp4" --title="标题" --tags="#春日，#随拍，#生活美学"

# 调试模式（详细日志）
node scripts/publish.js --video="视频.mp4" --title="标题" --debug
```

### 参数说明

| 参数 | 必需 | 说明 | 示例 |
|------|------|------|------|
| `--video` | ✅ | 视频文件路径 | `C:\Users\爽爽\Desktop\视频.mp4` |
| `--title` | ✅ | 视频标题 | `春日随拍｜城市日常` |
| `--tags` | ❌ | 话题标签（逗号分隔） | `#春日，#随拍，#生活美学` |
| `--debug` | ❌ | 调试模式 | `--debug` |
| `--profile` | ❌ | 浏览器 profile | `--profile=openclaw` |

### 默认话题

如果不指定 `--tags`，使用默认话题：
```
#生活美学 #日常文案 #我的生活碎片
```

---

## 📝 内容规范

### 标题要求

- **长度：** ≤20 字（超过会显示红色提示）
- **推荐格式：**
  - `主题｜副标题` - 例：春日随拍｜城市日常记录
  - `情绪词 + 对象` - 例：今天的好心情是咖啡给的

### 话题要求

- **数量：** 3-5 个
- **格式：** `#话题 1 #话题 2 #话题 3`
- **推荐话题：**
  - `#生活美学`
  - `#日常文案`
  - `#我的生活碎片`
  - `#每天都有值得记录的瞬间`
  - `#快乐瞬间`

### 视频要求

| 项目 | 要求 |
|------|------|
| **格式** | mp4, mov |
| **大小** | ≤20GB |
| **时长** | ≤4 小时 |
| **分辨率** | 建议 1080P 及以上 |

---

## 🔧 故障排除

### 浏览器超时

**错误信息：**
```
browser action timed out
```

**解决方法：**
```bash
# 1. 重启网关
gateway action=restart note="恢复浏览器服务"

# 2. 等待 2-3 秒

# 3. 重启浏览器
browser action=start

# 4. 重试发布
```

### 文件路径错误

**错误信息：**
```
Invalid path: must stay within uploads directory
```

**解决方法：**
```powershell
# 视频必须复制到 uploads 目录
Copy-Item "C:\路径\视频.mp4" `
  -Destination "C:\tmp\openclaw\uploads\视频.mp4" `
  -Force
```

### 选择器失效

**错误信息：**
```
element did not become interactive
```

**解决方法：**
1. 页面可能未完全加载，等待 3-5 秒后重试
2. 重新获取快照：`browser action=snapshot refs="aria"`
3. 使用新的 ref 重试

### 标题超限

**现象：** 输入框显示 `25/20` 红色提示

**解决方法：** 压缩标题到 20 字以内

### 发布后看不到视频

**原因：** 小红书需要审核

**解决：** 等待 5-30 分钟，然后在笔记管理页查看：
https://creator.xiaohongshu.com/note/manage

---

## 📊 发布成功标志

✅ **成功：**
- 页面返回上传页（https://creator.xiaohongshu.com/publish/publish）
- 笔记管理页显示"审核中"或"已发布"

❌ **失败：**
- 仍停留在编辑页
- 出现错误提示

---

## 🎯 高级用法

### 批量发布

```powershell
$videos = @(
  @{video="视频 1.mp4"; title="标题 1"; tags="#话题 1"},
  @{video="视频 2.mp4"; title="标题 2"; tags="#话题 2"},
  @{video="视频 3.mp4"; title="标题 3"; tags="#话题 3"}
)

foreach ($v in $videos) {
  node scripts/publish.js --video=$v.video --title=$v.title --tags=$v.tags
  Start-Sleep -Seconds 30  # 间隔 30 秒，避免触发风控
}
```

### 定时发布

使用 Windows 任务计划程序或 OpenClaw cron：

```bash
# 添加 cron 任务（每天 18:00 发布）
cron action=add job='{
  "name": "每日视频发布",
  "schedule": {"kind": "cron", "expr": "0 18 * * *"},
  "payload": {"kind": "agentTurn", "message": "发布今日视频"},
  "sessionTarget": "isolated"
}'
```

### 内容模板

创建 `config.json`：
```json
{
  "defaultTags": ["#生活美学", "#日常文案", "#我的生活碎片"],
  "titlePatterns": [
    "{主题}｜{副题}",
    "{情绪词}{对象}"
  ],
  "postTimes": ["18:00", "20:00", "22:00"]
}
```

---

## 📁 项目结构

```
xiaohongshu-video-publish/
├── SKILL.md              # 技能文档
├── README.md             # 使用说明（本文件）
├── package.json          # 依赖配置
├── scripts/
│   ├── publish.js        # 发布脚本
│   └── check-env.js      # 环境检查脚本
└── examples/
    └── config.json       # 配置示例
```

---

## 🔗 相关资源

- [OpenClaw 文档](https://docs.openclaw.ai)
- [小红书创作后台](https://creator.xiaohongshu.com/)
- [小红书发布规范](https://www.xiaohongshu.com/community)

---

## 📝 更新日志

### v1.1.0 (2026-03-20)
- ✅ 简化发布确认流程
- ✅ 添加浏览器超时自动恢复
- ✅ 优化 Windows 路径处理
- ✅ 添加完整错误处理

### v1.0.0 (2026-03-19)
- ✅ 初始版本
- ✅ 基础发布流程
- ✅ 标题和话题填写

---

## 💬 常见问题

**Q: 发布后多久能看到视频？**
A: 通常需要 5-30 分钟审核时间。

**Q: 支持图文发布吗？**
A: 本技能仅支持视频发布。图文请使用 `xiaohongshu-ops`。

**Q: 可以发布到抖音吗？**
A: 请使用 `douyin-video-upload` 技能。

**Q: 发布失败怎么办？**
A: 查看错误信息，参考"故障排除"章节。

---

## 📄 许可证

MIT License

---

**版本：** 1.1.0  
**最后更新：** 2026-03-20  
**测试状态：** ✅ 已验证（Windows 环境）  
**维护者：** Baoyu Skills Team
