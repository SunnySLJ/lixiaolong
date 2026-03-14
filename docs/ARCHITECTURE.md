# 项目架构文档

## 系统概述

视频自动化生产系统是一个基于 OpenClaw 的多模块协作平台，实现从热点抓取到视频发布的全流程自动化。

## 架构分层

### 1. 热点感知层

**职责：** 多平台热点数据采集

**组件：**
- TrendRadar 对接
- 智小红 API
- 智小抖 API
- 巨量算数爬虫

**输出：** 标准化热点数据结构

```json
{
  "id": "hotspot_001",
  "title": "话题标题",
  "source": "platform",
  "category": "分类",
  "heatScore": 95,
  "trend": "rising|stable|falling",
  "keywords": [],
  "createdAt": "ISO8601"
}
```

### 2. 数据分析层

**职责：** 热点分析、爆款结构提取

**组件：**
- NLP 语义分析
- 爆款结构提取
- 热点分类存储

**分析维度：**
- 标题模板
- 开头钩子
- 文案结构
- 视频时长
- 分镜节奏
- BGM 类型
- 发布时间

### 3. 内容生成层

**职责：** 文案脚本生成

**LLM 路由策略：**
```
Kimi (主力) → 批量文案、长文本
Claude (辅助) → 核心创意、高质量内容
OpenAI (备用) → 复杂逻辑
```

**生成内容：**
- 爆款标题（5-10 个变体）
- 完整文案脚本
- 分镜描述
- BGM 推荐

### 4. 素材管理层

**职责：** 素材存储、检索、管理

**存储架构：**
```
MinIO (对象存储)
├── video/
│   ├── by-industry/
│   ├── by-scene/
│   └── by-quality/
├── audio/
│   ├── bgm/
│   ├── sfx/
│   └── voice/
├── image/
│   ├── covers/
│   ├── stickers/
│   └── brands/
└── copy/
    ├── templates/
    ├── hooks/
    └── quotes/
```

**检索引擎：** Elasticsearch

**处理工具：**
- OpenCV - 图像处理
- OCR - 文字识别
- Whisper - 语音转文字

### 5. 视频生产层

**职责：** 视频剪辑、合成

**工作流程：**
1. 根据脚本匹配素材
2. FFmpeg 拼接视频
3. 添加转场和滤镜
4. 生成字幕
5. 合成 BGM
6. 生成封面
7. 质量检查

**工具栈：**
- FFmpeg - 视频处理
- OpenCV - 图像处理
- Whisper - 字幕生成

### 6. 发布运营层

**职责：** 多平台发布、数据监控

**支持平台：**
- 抖音
- 小红书
- B 站
- 视频号

**功能：**
- 定时发布
- 数据监控（播放、点赞、评论、转发）
- 效果分析
- A/B 测试
- 优化建议

## 数据流

```
[热点源] → [热点感知层] → [标准化数据]
                              ↓
                        [数据分析层]
                              ↓
                        [爆款结构库]
                              ↓
                        [内容生成层] → [文案脚本]
                              ↓
                        [素材管理层] → [匹配素材]
                              ↓
                        [视频生产层] → [成品视频]
                              ↓
                        [发布运营层] → [多平台]
                              ↓
                        [数据反馈] → [优化建议]
```

## Skill 架构

每个功能模块都是一个独立的 OpenClaw Skill：

```
skills/
├── skill-hotspot-fetch/    # 热点抓取
├── skill-hotspot-analyze/  # 热点分析
├── skill-copywrite-gen/    # 文案生成
├── skill-material-search/  # 素材检索
├── skill-material-ocr/     # OCR 识别
├── skill-video-edit/       # 视频混剪
├── skill-cover-gen/        # 封面生成
├── skill-platform-publish/ # 平台发布
├── skill-data-monitor/     # 数据监控
└── skill-optimize-suggest/ # 优化建议
```

每个 Skill 包含：
- `SKILL.md` - Skill 描述和文档
- `index.js` - 主逻辑代码
- `package.json` - 依赖配置
- `test.js` - 测试文件

## 配置管理

### 环境变量

所有敏感配置通过 `.env` 文件管理：

```bash
# LLM API
KIMI_API_KEY=
CLAUDE_API_KEY=

# 数据源 API
ZHIXIAOHONG_API_KEY=
ZHIXIAODOU_API_KEY=

# 存储
MINIO_ENDPOINT=
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=

# 发布平台
DOUYIN_COOKIE=
XIAOHONGSHU_COOKIE=
```

### 配置文件

```yaml
# config/app.yaml
app:
  name: lixiaolong
  version: 1.0.0
  logLevel: info

llm:
  primary: kimi
  secondary: claude
  fallback: openai

storage:
  type: minio
  endpoint: localhost:9000
  bucket: materials

video:
  outputFormat: mp4
  resolution: 1080p
  fps: 30
```

## 安全考虑

1. **API 密钥管理** - 使用环境变量，不提交到版本控制
2. **速率限制** - 所有外部 API 调用添加限流
3. **错误处理** - 完善的异常捕获和重试机制
4. **数据备份** - 定期备份素材库和配置
5. **权限控制** - 发布操作需要二次确认

## 扩展性

### 新增数据源

1. 在 `skills/skill-hotspot-fetch/` 中添加新的抓取函数
2. 在配置文件中注册新的数据源
3. 更新文档

### 新增 LLM

1. 在 `skills/skill-copywrite-gen/` 中添加新的模型适配器
2. 配置路由策略
3. 添加环境变量

### 新增发布平台

1. 创建 `skills/skill-platform-xxx/`
2. 实现平台 API 对接
3. 在主流程中注册

## 监控与日志

### 日志级别

- `debug` - 调试信息
- `info` - 一般信息
- `warn` - 警告
- `error` - 错误

### 关键指标

- 热点抓取成功率
- 文案生成质量评分
- 视频生产耗时
- 发布成功率
- 平台数据表现

## 性能优化

1. **缓存策略** - 热点数据、素材元数据缓存
2. **并行处理** - 多平台抓取并行执行
3. **队列管理** - 视频生产任务队列
4. **资源限制** - CPU、内存使用限制

---

**文档版本：** 1.0  
**最后更新：** 2026-03-14
