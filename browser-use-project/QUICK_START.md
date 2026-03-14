# 👑 皇上，API Key 配置指南

## 📋 当前状态

**✅ Browser-Use 已安装**  
**⏳ API Key 待配置**

---

## 🔑 获取 API Key（3 步搞定）

### 步骤 1：打开 Browser Use Cloud

**浏览器已打开：** https://cloud.browser-use.com/new-api-key

### 步骤 2：创建 API Key

1. 登录/注册账号
2. 点击 "Create New API Key" 或 "New API Key" 按钮
3. 给 Key 起个名字（例如："六位一体系统"）
4. **复制 API Key**（格式：`bu_xxxxxxxxxxxxxxxxx`）

### 步骤 3：配置到项目

**创建文件：** `C:\Users\爽爽\.openclaw\workspace\browser-use-project\.env`

**文件内容：**
```bash
BROWSER_USE_API_KEY=bu_xxxxxxxxxxxxxxxxx
```

---

## ✅ 验证配置

**运行测试：**
```bash
cd browser-use-project
uv run python test_browser_use.py
```

**预期结果：**
```
🌐 Browser-Use 测试开始...
✅ 完成！GitHub 上 browser-use 项目有 XXX 颗星
```

---

## 💰 费用说明

**新用户福利：**
- ✅ 免费试用额度
- ✅ 无需绑定信用卡

**定价（每 1M tokens）：**
- Input: $0.20
- Cached Input: $0.02
- Output: $2.00

**预估成本：**
- 简单任务：¥0.05-0.30
- 中等任务：¥0.30-1.50
- 复杂任务：¥1.50-7.00

---

## 🎯 在六位一体中的应用

### 1. 🔥 户部（热点感知）
```python
# 自动访问抖音、微博、小红书抓取热点
task = """
1. 访问抖音热榜
2. 记录前 10 个热点
3. 访问微博热搜
4. 整理成 JSON
"""
```

### 2. 📢 礼部（定时上传）
```python
# 自动登录并发布视频
task = """
1. 登录抖音
2. 上传视频
3. 填写标题和标签
4. 发布
"""
```

### 3. 📊 太子（数据分析）
```python
# 自动访问后台抓取数据
task = """
1. 访问抖音创作者后台
2. 查询视频数据
3. 生成分析报告
"""
```

---

## 📁 文件位置

| 文件 | 位置 |
|------|------|
| 项目目录 | `browser-use-project/` |
| 配置文件 | `browser-use-project/.env` |
| 测试脚本 | `test_browser_use.py` |
| 集成文档 | `INTEGRATION.md` |
| 配置指南 | `CONFIG_GUIDE.txt` |

---

## 🆘 需要帮助？

**文档：**
- [官方文档](https://docs.browser-use.com)
- [配置指南](API_KEY_SETUP.md)
- [集成文档](INTEGRATION.md)

**社区：**
- [Discord](https://link.browser-use.com/discord)
- [Twitter](https://x.com/intent/user?screen_name=browser_use)

---

## ⚡ 快速配置命令

```bash
# 1. 进入项目目录
cd C:\Users\爽爽\.openclaw\workspace\browser-use-project

# 2. 创建 .env 文件
echo BROWSER_USE_API_KEY=bu_xxx > .env

# 3. 运行测试
uv run python test_browser_use.py
```

---

**皇上，请：**
1. 在打开的浏览器页面获取 API Key
2. 创建 `.env` 文件并填入 API Key
3. 运行测试验证

**配置完成后告诉我，我帮您测试！** 🚀
