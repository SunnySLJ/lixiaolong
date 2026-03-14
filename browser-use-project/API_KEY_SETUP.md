# 🔑 Browser Use Cloud API Key 配置向导

## 📋 配置步骤

### 步骤 1：获取 API Key

**当前已打开页面：** https://cloud.browser-use.com/new-api-key

**操作步骤：**
1. 在打开的浏览器页面中登录/注册
2. 点击 "Create New API Key" 或 "New API Key"
3. 给 API Key 起个名字（例如："六位一体系统"）
4. 复制生成的 API Key（格式类似：`bu_xxxxxxxxxxxxxxxxxxxxxxxxx`）

---

### 步骤 2：配置到项目

**方式 A：使用配置文件（推荐）**

在项目根目录创建 `.env` 文件：

```bash
# .env
BROWSER_USE_API_KEY=bu_xxxxxxxxxxxxxxxxxxxxxxxxx

# 可选：其他 LLM 配置
# GOOGLE_API_KEY=your-google-key
# ANTHROPIC_API_KEY=your-anthropic-key
```

**方式 B：命令行配置**

```bash
cd browser-use-project
echo BROWSER_USE_API_KEY=bu_xxxxxxxxxxxxxxxxxxxxxxxxx > .env
```

---

### 步骤 3：验证配置

**运行测试脚本：**

```bash
cd browser-use-project
uv run python test_browser_use.py
```

**预期输出：**
```
🌐 Browser-Use 测试开始...

✅ 完成！结果：GitHub 上 browser-use 项目有 xxx 颗星
```

---

## 💰 定价说明

**ChatBrowserUse 模型定价（每 1M tokens）：**
- Input tokens: $0.20
- Cached input tokens: $0.02
- Output tokens: $2.00

**免费额度：**
- 新用户通常有免费试用额度
- 具体额度查看官网

**预估成本：**
- 简单任务（访问 1-2 个网页）：$0.01-0.05
- 中等任务（填写表单）：$0.05-0.20
- 复杂任务（多步骤操作）：$0.20-1.00

---

## 🔒 安全提示

**重要：**
- ⚠️ **不要** 将 API Key 提交到 Git
- ⚠️ **不要** 在公开场合分享 API Key
- ⚠️ **定期** 更换 API Key
- ⚠️ **监控** 使用情况，设置预算提醒

**.env 文件已自动加入 .gitignore：**
```bash
# .gitignore
.env
```

---

## 🛠️ 故障排查

### 问题 1：API Key 无效

**错误信息：**
```
Invalid API key
```

**解决方法：**
1. 检查 API Key 是否正确复制（包含 `bu_` 前缀）
2. 确认 API Key 未过期
3. 在官网检查 API Key 状态

### 问题 2：额度不足

**错误信息：**
```
Insufficient credits
```

**解决方法：**
1. 在官网充值
2. 检查使用量
3. 设置预算提醒

### 问题 3：网络问题

**错误信息：**
```
Connection timeout
```

**解决方法：**
1. 检查网络连接
2. 使用代理（如需要）
3. 重试

---

## 📊 使用监控

**在 Browser Use Cloud 控制台可以查看：**
- 📈 API 调用次数
- 💰 Token 消耗统计
- 📊 成本分析
- ⚠️ 异常检测

**控制台地址：** https://cloud.browser-use.com/dashboard

---

## 🎯 优化建议

### 1. 使用缓存
```python
# 启用缓存可以减少成本
agent = Agent(
    task="你的任务",
    llm=ChatBrowserUse(),
    browser=browser,
    generate_gif=False,  # 不生成 GIF 节省成本
)
```

### 2. 优化任务描述
```python
# 好的描述（更精准，花费更少）
task="访问 GitHub 搜索 browser-use 并返回 star 数量"

# 不好的描述（模糊，可能花费更多）
task="帮我看看 GitHub 上有个项目怎么样"
```

### 3. 设置超时和重试
```python
agent = Agent(
    task="你的任务",
    llm=ChatBrowserUse(),
    browser=browser,
    max_steps=10,  # 限制最大步骤数
)
```

---

## 📞 获取帮助

**官方文档：**
- [快速开始](https://docs.browser-use.com)
- [云服务文档](https://docs.cloud.browser-use.com)
- [定价详情](https://browser-use.com/pricing)

**社区支持：**
- [Discord](https://link.browser-use.com/discord)
- [Twitter](https://x.com/intent/user?screen_name=browser_use)

---

**配置完成后，运行测试脚本验证！** 🚀
