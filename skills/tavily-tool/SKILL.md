# Tavily Search Tool

Tavily AI 搜索工具 - 快速、准确的网络搜索 API

## 功能描述

使用 Tavily AI 进行智能网络搜索，获取高质量搜索结果。

## 环境变量

```bash
TAVILY_API_KEY=your_tavily_api_key
```

获取 API Key: https://app.tavily.com/

## 使用示例

```bash
# 搜索查询
openclaw skill run tavily-tool --params '{"query":"AI 最新进展","max_results":5}'
```

## 输入参数

```json
{
  "query": "搜索关键词",
  "max_results": 5,
  "include_answer": true,
  "include_raw_content": false
}
```

## 输出格式

```json
{
  "success": true,
  "answer": "AI 生成的答案摘要",
  "results": [
    {
      "title": "结果标题",
      "url": "https://...",
      "content": "内容摘要",
      "score": 0.95
    }
  ]
}
```
