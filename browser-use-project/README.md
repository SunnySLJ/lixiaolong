# Browser-Use 项目

🌐 让 AI 代理可以访问和操作网页

---

## 🚀 快速开始

### 1. 安装

```bash
# 已安装
uv add browser-use
uv sync
```

### 2. 配置环境变量（可选）

创建 `.env` 文件：

```bash
# Browser Use API Key（如需使用云服务）
BROWSER_USE_API_KEY=your-key

# Google API Key（可选）
GOOGLE_API_KEY=your-key

# Anthropic API Key（可选）
ANTHROPIC_API_KEY=your-key
```

### 3. 运行测试

```bash
uv run python test_browser_use.py
```

---

## 💡 使用示例

### 基础用法

```python
from browser_use import Agent, Browser, ChatBrowserUse
import asyncio

async def main():
    browser = Browser()
    
    agent = Agent(
        task="访问 GitHub 并搜索 browser-use 项目",
        llm=ChatBrowserUse(),
        browser=browser,
    )
    
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
```

### 使用不同模型

```python
from browser_use import Agent, Browser, ChatGoogle, ChatAnthropic

# 使用 Google Gemini
agent = Agent(
    task="你的任务",
    llm=ChatGoogle(model='gemini-2.0-flash-preview'),
    browser=browser,
)

# 使用 Claude
agent = Agent(
    task="你的任务",
    llm=ChatAnthropic(model='claude-sonnet-4-0'),
    browser=browser,
)
```

### 自定义工具

```python
from browser_use import Tools

tools = Tools()

@tools.action(description='搜索谷歌')
def google_search(query: str) -> str:
    return f"搜索结果：{query}"

agent = Agent(
    task="你的任务",
    llm=llm,
    browser=browser,
    tools=tools,
)
```

---

## 🎯 应用场景

### 1. 自动填写表单
### 2. 数据抓取
### 3. 自动化测试
### 4. 跨平台操作
### 5. 定时任务

---

## 📚 文档

- [官方文档](https://docs.browser-use.com)
- [云服务文档](https://docs.cloud.browser-use.com)
- [GitHub 仓库](https://github.com/browser-use/browser-use)

---

## 💰 定价

ChatBrowserUse 模型定价（每 1M tokens）：
- Input tokens: $0.20
- Cached input tokens: $0.02
- Output tokens: $2.00

---

**项目位置：** `C:\Users\爽爽\.openclaw\workspace\browser-use-project`
