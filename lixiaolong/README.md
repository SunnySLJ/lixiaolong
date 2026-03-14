# 六位一体·视频自动化生产系统

**GitHub:** https://github.com/SunnySLJ/lixiaolong  
**客户：** 帧龙虾  
**启动日期：** 2026-03-14  
**状态：** 开发中 🚀

---

## 🎯 项目概述

基于 OpenClaw 的**六位一体无人值守流水线**，实现从热点感知到数据分析的全流程自动化视频生产。

**核心能力：**
- 🔥 热点感知（<5 分钟响应）
- 📝 剧本创意（1000+/日）
- 🎬 素材匹配（<100ms）
- ⚔️ 批量生产（10 万+/日）
- 📢 定时上传（65+ 平台）
- 📊 数据分析（38 项指标，+300% 转化）

---

## 🏛️ 六位一体架构

```
皇上（您）
  ↓
【黄金三角】智能内容生产
  ↓
1. 💰 户部：热点感知（<5 分钟）
2. 📜 中书省：剧本创意（1000+/日）
3. 🔍 门下省：素材匹配（<100ms）
  ↓
【生产分发】自动化流水线
  ↓
4. ⚔️ 工部：批量生产（10 万+/日）
5. 📝 礼部：定时上传（65+ 平台）
6. 👑 太子：数据分析（38 项指标）
  ↓
🔄 数据驱动优化闭环
```

---

## 📋 7 个 Agent 角色

| 角色 | 职责 | 核心 KPI |
|------|------|----------|
| 👑 **皇上** | 决策者 | **您本人** |
| 👑 **太子** | 分拣调度 | 任务识别>95% |
| 📜 **中书省** | 规划文案 | 1000+ 脚本/日 |
| 🔍 **门下省** | 审核把关 | 质量评分>75 |
| ⚔️ **工部** | 执行开发 | 10 万+/日 |
| 💰 **户部** | 数据分析 | 38 项指标 |
| 📝 **礼部** | 文档发布 | 65+ 平台 |

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/SunnySLJ/lixiaolong.git
cd lixiaolong
```

### 2. 安装依赖

```bash
npm install
```

### 3. 配置环境变量

```bash
# 复制配置模板
cp .env.example .env

# 编辑 .env 填入 API 密钥
```

### 4. 配置 API Keys

```bash
# .env 文件
BROWSER_USE_API_KEY=bu_xxxxxxxxxxx
TAVILY_API_KEY=tvly-xxxxxxxxxx
KIMI_API_KEY=your_kimi_key
```

### 5. 运行第一个 Skill

```bash
# 热点抓取
openclaw skill run skill-hotspot-fetch

# Tavily 搜索
openclaw skill run tavily-tool --params '{"query":"AI 最新进展"}'
```

---

## 📁 项目结构

```
lixiaolong/
├── skills/                 # OpenClaw Skills
│   ├── skill-hotspot-fetch/    # 热点抓取 ✅
│   ├── skill-copywrite-gen/    # 文案生成 ✅
│   ├── skill-material-search/  # 素材检索 ✅
│   ├── skill-video-edit/       # 视频混剪 ✅
│   ├── tavily-tool/            # Tavily 搜索 ✅
│   └── ...
├── agents/                 # 7 个 Agent 配置
│   ├── taizi/                # 太子（数据分析）
│   ├── zhongshu/             # 中书省（剧本创意）
│   ├── menxia/               # 门下省（审核把关）
│   ├── gongbu/               # 工部（批量生产）
│   ├── hubu/                 # 户部（热点感知）
│   └── libu/                 # 礼部（定时上传）
├── docs/                   # 完整文档
│   ├── 6_IN_1_OVERVIEW.md    # 六位一体总览
│   ├── 6_IN_1_PIPELINE.md    # 流水线设计
│   ├── 7_AGENTS_DESIGN.md    # 7 Agent 设计
│   └── ...
├── browser-use-project/    # Browser-Use 集成
├── edict/                  # 三省六部制系统
└── dashboard/              # 看板界面
```

---

## 🛠️ 技术栈

### 核心框架
- **OpenClaw** - Agent 调度框架
- **Node.js** - 主要运行时
- **Python 3.9+** - 数据处理

### AI 模型
- **Kimi** - 主力文案生成（成本低 + 中文强）
- **Claude** - 核心创意生成
- **ChatBrowserUse** - 浏览器自动化
- **Tavily** - 智能搜索

### 视频处理
- **FFmpeg** - 视频混剪
- **OpenCV** - 图像处理
- **Whisper** - 语音识别

### 数据存储
- **MinIO** - 对象存储
- **Elasticsearch** - 素材检索
- **Metabase** - 数据看板

---

## 📊 Skills 列表

| Skill | 功能 | 状态 |
|-------|------|------|
| skill-hotspot-fetch | 热点抓取 | ✅ |
| skill-copywrite-gen | 文案生成 | ✅ |
| skill-material-search | 素材检索 | ✅ |
| skill-video-edit | 视频混剪 | ✅ |
| tavily-tool | Tavily 搜索 | ✅ |
| skill-platform-publish | 平台发布 | ⏳ |
| skill-data-monitor | 数据监控 | ⏳ |

---

## 🎯 实施路线图

### 第一阶段：MVP（2-3 周）
- [x] 搭建基础框架（OpenClaw + Skill 架构）
- [x] 实现热点抓取（7 个平台）
- [x] LLM 文案生成（Kimi API 对接）
- [x] 基础素材库
- [ ] 手动确认 + FFmpeg 混剪
- [ ] 输出第一条自动化视频

### 第二阶段：自动化（3-4 周）
- [ ] 智小红/智小抖 API 对接
- [ ] 爆款结构库建设
- [ ] MinIO 素材存储系统
- [ ] OCR 字幕提取
- [ ] 定时任务调度
- [ ] 数据监控看板

### 第三阶段：智能化（4-6 周）
- [ ] 语义素材匹配
- [ ] 多 LLM 智能路由
- [ ] 自动封面生成
- [ ] 多平台 API 发布
- [ ] A/B 测试框架
- [ ] 效果反馈闭环

---

## 💰 资源配置

### API 成本
- Kimi: ~¥200/月
- Claude: ~¥500/月
- Browser Use: $0.20/1M tokens
- Tavily: 免费 1000 次/月

### 存储
- MinIO 服务器 1TB: ~¥100/月

### 计算
- 视频渲染：本地 GPU 或云服务器

---

## ⚠️ 风险与应对

| 风险 | 影响 | 应对方案 |
|------|------|----------|
| 平台 API 限制 | 高 | 准备多账号 + 爬虫备用 |
| 素材版权 | 高 | 优先 Pexels 等免版权源 |
| 内容同质化 | 中 | 人工审核 + 创意注入 |
| LLM 输出不稳定 | 中 | 多模型冗余 + 人工校验 |
| 视频质量波动 | 中 | 建立质量检查清单 |

---

## 📚 相关文档

- [六位一体总览](docs/6_IN_1_OVERVIEW.md)
- [流水线设计](docs/6_IN_1_PIPELINE.md)
- [7 Agent 设计](docs/7_AGENTS_DESIGN.md)
- [Browser-Use 集成](browser-use-project/README.md)
- [Tavily 配置](skills/tavily-tool/README.md)

---

## 🔗 相关链接

- [OpenClaw 文档](https://docs.openclaw.ai)
- [Browser-Use](https://github.com/browser-use/browser-use)
- [Tavily](https://tavily.com/)
- [TrendRadar](https://github.com/sansan0/TrendRadar)

---

## 👥 团队

- **客户：** 帧龙虾
- **启动日期：** 2026-03-14
- **技术栈：** OpenClaw + Node.js + Python

---

## 📄 许可证

MIT License

---

## 📊 项目进度

**查看实时进度：**
- 📁 `S:\项目进度跟踪.html`
- 📊 GitHub Issues

---

**最后更新：** 2026-03-14  
**状态：** 开发中 🚀
