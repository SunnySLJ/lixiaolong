# 安装指南 - 小红书视频发布技能

## ✅ 创建完成！

技能位置：`C:\Users\爽爽\.openclaw\workspace\skills\xiaohongshu-video-publish`

---

## 📦 文件结构

```
xiaohongshu-video-publish/
├── SKILL.md              # 技能文档（4.4 KB）
├── README.md             # 使用说明（4.9 KB）
├── INSTALL.md            # 安装指南（本文件）
├── package.json          # 依赖配置
├── scripts/
│   ├── publish.js        # 发布脚本（7.1 KB）
│   └── check-env.js      # 环境检查（2.7 KB）
├── examples/
│   └── config.json       # 配置示例（1.1 KB）
└── node_modules/         # 依赖包（npm install 后生成）
```

---

## 🔧 安装步骤

### 1. 确认环境要求

| 项目 | 版本 | 检查命令 |
|------|------|----------|
| Node.js | >=18.0.0 | `node --version` |
| OpenClaw | >=2026.3.0 | `openclaw status` |
| npm | >=9.0.0 | `npm --version` |

### 2. 安装依赖

```bash
cd C:\Users\爽爽\.openclaw\workspace\skills\xiaohongshu-video-publish
npm install
```

✅ 已完成（539 个包）

### 3. 环境检查

```bash
node scripts/check-env.js
```

**预期输出：**
```
✅ Node.js v22.22.1
✅ C:\tmp\openclaw\uploads
✅ C:\Users\爽爽\.openclaw\workspace
✅ SKILL.md
✅ package.json
✅ scripts/publish.js
```

---

## 🚀 使用方法

### 方式 1：直接对话（推荐）

告诉我要发布的内容：
```
帮我发小红书，视频在 C:\Users\爽爽\Desktop\视频.mp4，标题是「春日随拍」
```

### 方式 2：使用脚本

```bash
# 基础发布
node scripts/publish.js --video="视频路径" --title="标题"

# 带话题
node scripts/publish.js --video="视频.mp4" --title="标题" --tags="#春日，#随拍"

# 调试模式
node scripts/publish.js --video="视频.mp4" --title="标题" --debug
```

---

## ⚠️ 必需约束

### 1. 视频文件
- **格式：** mp4 或 mov
- **大小：** ≤20GB
- **路径：** 自动复制到 `C:\tmp\openclaw\uploads\`

### 2. 浏览器
- **Profile：** `openclaw`（内置浏览器）
- **登录：** 需提前登录小红书创作后台
- **URL：** https://creator.xiaohongshu.com/

### 3. 内容规范
- **标题：** ≤20 字
- **话题：** 3-5 个，格式 `#话题 1 #话题 2`

---

## 🔗 分享给别人

### 方式 1：复制整个目录

```bash
# 打包技能
cd C:\Users\爽爽\.openclaw\workspace\skills
tar -czf xiaohongshu-video-publish.tar.gz xiaohongshu-video-publish/

# 发送给别人，对方解压到他们的 skills 目录
```

### 方式 2：发布到 ClawHub

```bash
# 安装 clawhub CLI
npm install -g clawhub

# 发布技能
cd xiaohongshu-video-publish
clawhub publish
```

### 方式 3：GitHub 仓库

```bash
# 推送到 GitHub
git init
git add .
git commit -m "小红书视频发布技能"
git remote add origin <你的仓库>
git push -u origin main
```

别人可以安装：
```bash
clawhub install <你的 GitHub 用户名>/xiaohongshu-video-publish
```

---

## 📝 给别人用的安装说明

### 快速安装

```bash
# 1. 克隆或复制技能到 OpenClaw workspace
cd <OpenClaw workspace>/skills
git clone <仓库 URL> xiaohongshu-video-publish

# 2. 安装依赖
cd xiaohongshu-video-publish
npm install

# 3. 检查环境
node scripts/check-env.js

# 4. 开始使用
node scripts/publish.js --video="视频.mp4" --title="标题"
```

### 环境要求

1. **Node.js >=18.0.0** - [下载](https://nodejs.org/)
2. **OpenClaw >=2026.3.0** - [安装指南](https://docs.openclaw.ai)
3. **小红书账号** - 已登录创作后台

---

## 💡 常见问题

**Q: 别人没有 OpenClaw 能用吗？**
A: 不能。这个技能依赖 OpenClaw 的浏览器工具。

**Q: 可以发布到抖音吗？**
A: 不可以。这是小红书专用技能。抖音请用 `douyin-video-upload`。

**Q: 支持 macOS/Linux 吗？**
A: 支持。路径会自动适配（`package.json` 中已配置）。

**Q: 如何更新技能？**
A: 重新拉取代码并运行 `npm install`。

---

## 📄 许可证

MIT License

---

**版本：** 1.1.0  
**创建日期：** 2026-03-20  
**维护者：** Baoyu Skills Team
