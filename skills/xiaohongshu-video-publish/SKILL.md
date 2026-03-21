---
name: xiaohongshu-video-publish
description: 小红书视频一键发布技能。使用 OpenClaw 内置浏览器自动上传视频、填写标题和话题并发布。
---

# 小红书视频一键发布技能

## 📋 前置要求

### 必需环境
1. **OpenClaw** - 已安装并运行
2. **浏览器服务** - OpenClaw 内置浏览器（profile: `openclaw`）
3. **小红书登录** - 已在浏览器中登录小红书创作后台

### 安装检查清单
```bash
# 1. 检查 OpenClaw 是否运行
openclaw status

# 2. 检查浏览器服务
browser action=status

# 3. 确认小红书已登录
# 手动访问：https://creator.xiaohongshu.com/
# 确认能看到"爽叔探世界"（或你的账号名）
```

### 依赖安装（可选）
如需批量处理视频，可安装以下依赖：
```bash
cd C:\Users\爽爽\.openclaw\workspace\skills\xiaohongshu-video-publish
npm install
```

---

## 🚀 快速开始

### 方式 1：直接对话（推荐）
告诉我要发布的内容：
```
帮我发小红书，视频在 C:\Users\爽爽\Desktop\视频.mp4，标题是「春日随拍」
```

### 方式 2：使用脚本
```powershell
# 基础发布
node scripts/publish.js --video="视频路径" --title="标题"

# 带话题发布
node scripts/publish.js --video="视频路径" --title="标题" --tags="#话题 1,#话题 2"

# 调试模式
node scripts/publish.js --video="视频路径" --title="标题" --debug
```

---

## 📝 执行流程

### 1. 环境检查
- ✅ 检查浏览器状态
- ✅ 确认小红书创作后台可访问
- ✅ 验证视频文件存在

### 2. 准备视频
- 复制视频到 `C:\tmp\openclaw\uploads\` 目录
- 验证视频格式（mp4/mov）
- 验证文件大小（≤20GB）

### 3. 上传视频
- 打开小红书创作后台
- 导航到发布页
- 上传视频文件
- 等待上传完成（15 秒）

### 4. 填写内容
- 填写标题（≤20 字最佳）
- 填写话题标签（3-5 个）
- 可选：设置封面

### 5. 发布
- 点击发布按钮
- 等待发布处理（8 秒）
- 确认发布成功（页面返回上传页）

---

## 📋 内容规范

### 标题
- **长度：** ≤20 字（出现超限提示需压缩）
- **格式：** `主题｜副标题` 或 `情绪词 + 具体对象`
- **示例：**
  - ✅ 春日随拍小片段｜城市日常记录
  - ✅ 今天的好心情是咖啡给的
  - ❌ 太长了这个标题超过 20 个字了

### 话题标签
- **数量：** 3-5 个
- **格式：** `#话题 1 #话题 2 #话题 3`
- **推荐：**
  - `#生活美学`
  - `#日常文案`
  - `#我的生活碎片`
  - `#每天都有值得记录的瞬间`

### 视频要求
- **格式：** mp4, mov
- **大小：** ≤20GB
- **时长：** ≤4 小时
- **分辨率：** 建议 1080P 及以上

---

## 🔧 脚本参数

### 必需参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `--video` | 视频文件路径 | `C:\Users\爽爽\Desktop\视频.mp4` |
| `--title` | 视频标题 | `春日随拍` |

### 可选参数
| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `--tags` | 话题标签（逗号分隔） | `#生活美学 #日常文案` | `#春日，#随拍` |
| `--debug` | 调试模式（详细日志） | `false` | `--debug` |
| `--profile` | 浏览器 profile | `openclaw` | `--profile=openclaw` |
| `--cover` | 封面图片路径 | 自动截取第一帧 | `C:\cover.jpg` |

---

## ⚠️ 错误处理

### 浏览器超时
**现象：** `browser action` 返回 timeout 错误

**解决：**
```bash
# 重启网关
gateway action=restart note="恢复浏览器服务"

# 等待 2-3 秒后重试
browser action=start
```

### 文件路径错误
**现象：** `Invalid path: must stay within uploads directory`

**解决：**
```powershell
# 必须复制到 uploads 目录
Copy-Item "视频路径" -Destination "C:\tmp\openclaw\uploads\视频.mp4" -Force
```

### 选择器失效
**现象：** `element did not become interactive`

**解决：**
```
# 重新获取页面快照
browser action=snapshot refs="aria"
# 使用新的 ref 重试
```

### 标题超限
**现象：** 输入框显示 `25/20` 红色提示

**解决：** 压缩标题到 20 字以内

---

## 📊 发布成功标志

✅ **成功：** 页面返回上传页（https://creator.xiaohongshu.com/publish/publish）

❌ **失败：** 仍停留在编辑页或出现错误提示

**验证方法：**
1. 导航到笔记管理页：https://creator.xiaohongshu.com/note/manage
2. 查看最新笔记状态
3. 状态为"审核中"或"已发布" = 成功

---

## 🎯 最佳实践

### 1. 批量发布
```powershell
# 准备多个视频
$videos = @(
  @{video="视频 1.mp4"; title="标题 1"; tags="#话题 1"},
  @{video="视频 2.mp4"; title="标题 2"; tags="#话题 2"}
)

# 循环发布
foreach ($v in $videos) {
  node scripts/publish.js --video=$v.video --title=$v.title --tags=$v.tags
  Start-Sleep -Seconds 30  # 间隔 30 秒
}
```

### 2. 定时发布
使用 OpenClaw cron 定时任务：
```bash
cron action=add job='{
  "name": "每日视频发布",
  "schedule": {"kind": "cron", "expr": "0 18 * * *"},
  "payload": {"kind": "agentTurn", "message": "发布今日视频"},
  "sessionTarget": "isolated"
}'
```

### 3. 内容模板
创建内容模板文件：
```json
{
  "defaultTags": ["#生活美学", "#日常文案", "#我的生活碎片"],
  "titlePatterns": ["{主题}｜{副题}", "{情绪词}{对象}"],
  "postTimes": ["18:00", "20:00", "22:00"]
}
```

---

## 📁 文件结构

```
xiaohongshu-video-publish/
├── SKILL.md              # 技能文档（本文件）
├── README.md             # 使用说明
├── package.json          # 依赖配置
├── scripts/
│   ├── publish.js        # 发布脚本
│   └── check-env.js      # 环境检查脚本
└── examples/
    └── example-config.json  # 配置示例
```

---

## 🔗 相关技能

- **xiaohongshu-ops** - 小红书全链路运营（包含发布、回复、分析）
- **douyin-video-upload** - 抖音视频上传
- **baoyu-cover-image** - 封面图生成

---

## 📝 更新日志

### v1.1 (2026-03-20)
- ✅ 简化发布确认流程（返回上传页 = 成功）
- ✅ 添加浏览器超时自动恢复
- ✅ 优化文件路径处理（Windows 兼容）
- ✅ 添加完整错误处理

### v1.0 (2026-03-19)
- ✅ 初始版本
- ✅ 基础发布流程
- ✅ 标题和话题填写

---

## 💡 常见问题

**Q: 发布后看不到视频？**
A: 小红书需要审核，通常 5-30 分钟。可在笔记管理页查看状态。

**Q: 可以定时发布吗？**
A: 可以，使用 `--schedule` 参数或配置 cron 任务。

**Q: 支持图文发布吗？**
A: 本技能仅支持视频发布。图文发布请使用 `xiaohongshu-ops`。

**Q: 发布失败怎么办？**
A: 检查浏览器是否登录、视频格式是否正确、网络连接是否正常。

---

**版本：** 1.1  
**最后更新：** 2026-03-20  
**测试状态：** ✅ 已验证（Windows 环境，视频 2.mp4 成功发布）  
**维护者：** Baoyu Skills Team
