# Browser-Use 集成指南

## 🎯 在六位一体系统中的应用

Browser-Use 可以增强以下环节：

### 1. 🔥 热点感知（户部）
- 自动访问各大平台抓取热点
- 模拟真人操作，避免被封禁
- 跨平台数据采集

### 2. 📢 定时上传（礼部）
- 自动登录多平台
- 模拟真人发布视频
- 处理验证码和登录验证

### 3. 📊 数据分析（太子）
- 自动访问各平台后台
- 抓取播放/转化数据
- 生成分析报告

---

## 💻 安装位置

**项目路径：** `C:\Users\爽爽\.openclaw\workspace\browser-use-project`

**启动方式：**
```bash
# 方式 1: 运行测试脚本
cd browser-use-project
uv run python test_browser_use.py

# 方式 2: 使用启动脚本
start.bat

# 方式 3: 交互式 CLI
uvx browser-use
```

---

## 🔧 集成示例

### 示例 1：自动抓取热点

```python
from browser_use import Agent, Browser, ChatBrowserUse
import asyncio

async def fetch_hotspots():
    browser = Browser()
    
    agent = Agent(
        task="""
        1. 访问抖音热榜 (https://www.douyin.com/hot)
        2. 记录前 10 个热点话题
        3. 访问微博热搜 (https://s.weibo.com/top/summary)
        4. 记录前 10 个热搜
        5. 整理成 JSON 格式返回
        """,
        llm=ChatBrowserUse(),
        browser=browser,
    )
    
    result = await agent.run()
    return result

# 在户部中使用
# from fetch_hotspots import fetch_hotspots
# hotspots = asyncio.run(fetch_hotspots())
```

### 示例 2：自动发布视频

```python
async def publish_video(video_path, platforms=['douyin', 'xiaohongshu']):
    browser = Browser()
    
    agent = Agent(
        task=f"""
        1. 登录{platforms[0]}
        2. 上传视频：{video_path}
        3. 填写标题和标签
        4. 选择最佳发布时间
        5. 点击发布
        """,
        llm=ChatBrowserUse(),
        browser=browser,
    )
    
    await agent.run()

# 在礼部中使用
```

### 示例 3：自动分析数据

```python
async def analyze_performance(video_ids):
    browser = Browser()
    
    agent = Agent(
        task=f"""
        1. 访问抖音创作者后台
        2. 查询视频 {video_ids} 的数据
        3. 记录播放量、点赞、评论、转发
        4. 计算转化率
        5. 生成分析报告
        """,
        llm=ChatBrowserUse(),
        browser=browser,
    )
    
    result = await agent.run()
    return result

# 在太子中使用
```

---

## 📋 配置说明

### 环境变量

创建 `.env` 文件：

```bash
# Browser Use API Key（推荐使用云服务）
BROWSER_USE_API_KEY=your-api-key

# 或使用本地模型
# GOOGLE_API_KEY=your-key
# ANTHROPIC_API_KEY=your-key
```

### 使用真实浏览器配置

```python
from browser_use import Browser

browser = Browser(
    use_cloud=True,  # 使用云服务（推荐）
    # 或使用本地配置
    # use_cloud=False,
    # headless=False,
    # user_data_dir="./chrome-profile"
)
```

---

## 🎯 最佳实践

### 1. 使用云服务
- 更快的执行速度
- 更好的防检测能力
- 自动处理验证码

### 2. 重用浏览器配置
- 保存登录状态
- 避免频繁登录
- 提高账号安全性

### 3. 错误处理
```python
try:
    result = await agent.run()
except Exception as e:
    print(f"执行失败：{e}")
    # 重试或回退方案
```

---

## 📊 性能对比

| 方式 | 速度 | 稳定性 | 防检测 | 成本 |
|------|------|--------|--------|------|
| Browser-Use Cloud | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 付费 |
| Browser-Use 本地 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | 免费 |
| 传统 Selenium | ⭐⭐ | ⭐⭐ | ⭐ | 免费 |

---

## 🚀 下一步

1. **配置 API Key** - 获取 Browser Use Cloud API Key
2. **测试基本功能** - 运行测试脚本
3. **集成到系统** - 在户部/礼部/太子中使用
4. **优化性能** - 根据实际需求调整配置

---

**文档位置：** `browser-use-project/INTEGRATION.md`
