# Tavily Search Tool 配置指南

## 📋 配置步骤

### 步骤 1：获取 API Key

1. 访问 https://app.tavily.com/
2. 注册/登录账号
3. 在 Dashboard 中获取 API Key
4. 复制 API Key（格式类似：`tvly-xxxxxxxxxxxxxxxx`）

### 步骤 2：配置环境变量

**方式 A：项目 .env 文件**

在 `C:\Users\爽爽\.openclaw\workspace\.env` 中添加：

```bash
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxx
```

**方式 B：系统环境变量**

```bash
# Windows PowerShell
$env:TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxx"

# 或永久添加到系统环境变量
setx TAVILY_API_KEY "tvly-xxxxxxxxxxxxxxxx"
```

### 步骤 3：测试

```bash
cd skills/tavily-tool
node test.js
```

---

## 💰 定价说明

**免费额度：**
- 每月 1000 次搜索
- 适合开发和测试

**付费计划：**
- Starter: $29/月，10,000 次
- Pro: $99/月，50,000 次
- Enterprise: 定制

---

## 🎯 在六位一体中的应用

### 1. 🔥 户部（热点感知）
```python
# 搜索全网热点
task = "搜索 AI 领域最新热点话题"
```

### 2. 📊 太子（数据分析）
```python
# 搜索竞品数据
task = "搜索竞品分析报告"
```

### 3. 📝 礼部（文档发布）
```python
# 搜索相关资料
task = "搜索行业报告用于文档编写"
```

---

## 📁 文件位置

| 文件 | 位置 |
|------|------|
| Skill 代码 | `skills/tavily-tool/` |
| 主逻辑 | `skills/tavily-tool/index.js` |
| 文档 | `skills/tavily-tool/SKILL.md` |
| 测试 | `skills/tavily-tool/test.js` |

---

## 🚀 使用示例

### OpenClaw 调用

```bash
openclaw skill run tavily-tool --params '{"query":"AI 最新进展","max_results":5}'
```

### 程序化调用

```javascript
const tavily = require('./skills/tavily-tool');

const result = await tavily.main({
  query: 'AI 最新进展 2026',
  max_results: 5
});

console.log(result);
```

---

**配置完成后运行测试脚本验证！** 🚀
