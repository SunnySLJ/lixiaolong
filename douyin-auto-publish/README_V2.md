# 🎬 抖音发布工具 v0.2.0

> 支持官方 API + 网页自动化两种方式

[![Status](https://img.shields.io/badge/status-ready-success)]()
[![Version](https://img.shields.io/badge/version-0.2.0-blue)]()
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://python.org)

---

## ✨ 特性

### 🏢 官方 API 方式

**适合企业/MCN 机构**

- ✅ 稳定可靠，官方支持
- ✅ 不易触发风控
- ✅ 支持批量管理
- ✅ 可获取详细数据
- ❌ 需要企业资质
- ❌ 申请周期 1-2 周

### 🤖 网页自动化方式

**适合个人用户**

- ✅ 无需资质，立即可用
- ✅ 零成本
- ✅ 快速部署
- ❌ 可能触发风控
- ❌ 需要维护登录状态

---

## 🚀 快速开始

### 1. 安装依赖

```bash
cd douyin-auto-publish
pip install -r requirements.txt
```

### 2. 选择使用方式

#### 方式 A：官方 API（推荐企业）

**步骤：**

1. **申请资质**（1-2 周）
   - 访问 https://open.douyin.com/
   - 注册企业账号
   - 提交资质认证
   - 创建应用
   - 获取 `client_key` 和 `client_secret`

2. **配置**
   ```bash
   # 编辑 config.json
   {
     "douyin_openapi": {
       "enabled": true,
       "client_key": "你的 client_key",
       "client_secret": "你的 client_secret"
     }
   }
   ```

3. **OAuth 授权**
   ```bash
   streamlit run web_ui.py
   # 在浏览器中打开，点击"开始 OAuth 授权"
   ```

4. **发布视频**
   ```python
   from douyin_openapi import DouyinOpenAPI
   
   client = DouyinOpenAPI("client_key", "client_secret")
   # 先完成 OAuth 授权获取 access_token
   
   # 一键发布
   result = client.publish_video_file(
       video_path="./video.mp4",
       title="视频标题",
       description="描述 #话题"
   )
   ```

#### 方式 B：网页自动化（推荐个人）

**步骤：**

1. **配置**（无需修改，默认已启用）

2. **登录抖音**
   ```bash
   python scripts/quick_login.py
   ```
   - 自动打开浏览器
   - 使用抖音 APP 扫码登录
   - Cookie 自动保存

3. **发布视频**
   ```bash
   python scripts/publish.py \
     --video ./storage/videos/test.mp4 \
     --title "视频标题" \
     --desc "视频描述 #话题 #标签"
   ```

---

## 📖 功能说明

### 1. 官方 API 核心功能

#### OAuth 授权

```python
from douyin_openapi import DouyinOpenAPI

client = DouyinOpenAPI(client_key, client_secret)

# 获取授权 URL
oauth_url = client.get_oauth_url("http://localhost:8000/callback")
print(f"请在浏览器打开：{oauth_url}")

# 用户授权后，获取 code
code = input("请输入授权码：")

# 换取 access_token
result = client.get_access_token(code, "http://localhost:8000/callback")
print(f"access_token: {client.access_token}")
```

#### 上传视频

```python
result = client.upload_video(
    video_path="./video.mp4",
    title="视频标题"
)

if result.get("error_code") == 0:
    video_id = result["data"]["video_id"]
    print(f"上传成功，video_id: {video_id}")
```

#### 发布视频

```python
result = client.create_video(
    video_id="xxx",
    text="视频标题 描述 #话题",
    poi_id="xxx",  # 可选：地理位置
    micro_app_id="xxx"  # 可选：小程序
)
```

#### 一键发布

```python
result = client.publish_video_file(
    video_path="./video.mp4",
    title="标题",
    description="描述 #话题"
)
```

#### 视频管理

```python
# 获取视频列表
videos = client.list_videos(count=20)

# 获取视频数据
data = client.get_video_data(video_id="xxx")

# 删除视频
result = client.delete_video(video_id="xxx")
```

### 2. 网页自动化核心功能

#### 登录

```bash
python scripts/quick_login.py
```

#### 发布

```bash
python scripts/publish.py \
  --video ./video.mp4 \
  --title "标题" \
  --desc "描述 #话题" \
  --privacy public  # public/friend/private
```

#### Python 调用

```python
from publisher.douyin_publisher import DouyinPublisher

publisher = DouyinPublisher()

# 检查登录
if await publisher.check_login("default"):
    # 发布
    result = await publisher.publish(
        video_path="./video.mp4",
        title="标题",
        description="描述 #话题"
    )
```

---

## 🌐 Web 管理界面

### 启动

```bash
streamlit run web_ui.py
```

### 功能

1. **📋 控制台**
   - 状态概览
   - 快速操作
   - 最近发布记录

2. **⚙️ 官方 API 配置**
   - 配置 client_key/client_secret
   - OAuth 授权管理
   - Token 状态查看

3. **🤖 网页自动化**
   - 浏览器配置
   - 登录状态检查
   - Cookie 管理

4. **📹 发布视频**
   - 选择视频文件
   - 填写标题描述
   - 选择发布方式
   - 一键发布

5. **📊 视频管理**
   - 查看已发布视频
   - 获取视频数据
   - 删除视频

---

## 📁 项目结构

```
douyin-auto-publish/
├── douyin_openapi.py        # 官方 API 客户端 ⭐
├── web_ui.py                # Web 管理界面 ⭐
├── config.json              # 配置文件
├── publisher/
│   └── douyin_publisher.py  # 网页自动化发布器
├── scripts/
│   ├── quick_login.py       # 快速登录
│   ├── publish.py           # 发布脚本
│   └── ...
├── storage/
│   ├── cookies/             # Cookie 存储
│   ├── videos/              # 视频文件
│   └── logs/                # 日志
├── requirements.txt         # Python 依赖
└── README.md               # 本文件
```

---

## 🔑 配置说明

### config.json

```json
{
  "douyin_openapi": {
    "enabled": false,          // 是否启用官方 API
    "client_key": "xxx",       // 必填：企业申请
    "client_secret": "xxx",    // 必填：企业申请
    "redirect_uri": "http://localhost:8000/callback",
    "access_token": "",        // OAuth 授权后自动填充
    "refresh_token": "",
    "token_expires_at": 0
  },
  
  "web_automation": {
    "enabled": true,           // 是否启用网页自动化
    "browser": "chrome",
    "debug_port": 9222,
    "headless": false
  },
  
  "publish_settings": {
    "default_title_prefix": "",
    "default_hashtags": ["#AI", "#自动化"],
    "auto_retry": true,
    "retry_times": 3
  },
  
  "storage": {
    "videos_path": "./storage/videos",
    "cookies_path": "./storage/cookies",
    "logs_path": "./logs"
  }
}
```

---

## ⚠️ 注意事项

### 官方 API

1. **资质要求**
   - 仅限企业/MCN 机构
   - 个人无法申请
   - 审核周期 1-2 周

2. **使用限制**
   - 视频大小 ≤ 4GB
   - 时长 ≤ 15 分钟
   - 推荐 16:9 竖版视频

3. **合规要求**
   - 遵守抖音平台规则
   - 不发布违规内容
   - 不携带违规水印

### 网页自动化

1. **账号安全**
   - 控制发布频率（< 5 条/天）
   - 使用真实网络环境
   - 定期更新登录状态

2. **风控风险**
   - 可能触发抖音风控
   - 建议使用小号测试
   - 不要使用代理

3. **维护成本**
   - 页面更新需要维护
   - 选择器可能失效
   - 需要定期检查

---

## 🔗 相关资源

### 官方文档

- [抖音开放平台](https://open.douyin.com/)
- [内容发布方案](https://open.douyin.com/platform/resource/docs/ability/content-management/douyin-publish-solution/)
- [上传视频接口](https://open.douyin.com/api/douyin/v1/video/upload_video/)
- [发布视频接口](https://open.douyin.com/api/douyin/v1/video/create/)

### 参考项目

- [MoneyPrinterPlus](https://github.com/ddean2009/MoneyPrinterPlus) - AI 视频生成 + 自动发布
- [matrix](https://github.com/whitescent/matrix) - 多平台矩阵发布

---

## 📊 方案对比

| 功能 | 官方 API | 网页自动化 |
|------|----------|------------|
| 资质要求 | 企业/MCN | 无 |
| 成本 | 中 | 低 |
| 稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 功能完整性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 批量管理 | ✅ | ⚠️ |
| 数据统计 | ✅ | ❌ |
| 删除视频 | ✅ | ❌ |
| 开发周期 | 1-2 周 | 1 天 |

---

## 🎯 推荐使用场景

### 选择官方 API，如果你：

- ✅ 是企业/MCN 机构
- ✅ 需要批量管理视频
- ✅ 需要获取详细数据
- ✅ 追求稳定可靠

### 选择网页自动化，如果你：

- ✅ 是个人用户
- ✅ 想立即使用
- ✅ 发布量不大
- ✅ 预算有限

---

## 💡 最佳实践

### 混合方案（推荐）

**主账号**：使用官方 API
- 稳定可靠
- 发布重要内容
- 批量管理

**小号/测试号**：使用网页自动化
- 灵活快速
- 测试新功能
- 补充发布

---

## 🆘 常见问题

### Q1: 个人能申请官方 API 吗？

**A**: 不能。官方 API 需要企业资质，个人账号无法申请。

### Q2: 网页自动化会被封号吗？

**A**: 有可能。如果频繁操作或触发风控，可能被封号。建议：
- 控制发布频率（< 5 条/天）
- 使用真实网络环境
- 不要使用代理
- 定期更新登录状态

### Q3: 官方 API 收费吗？

**A**: 目前免费。但需要企业资质。

### Q4: 两种方案可以同时使用吗？

**A**: 可以。建议主账号用官方 API，小号用网页自动化。

---

## 📝 更新日志

### v0.2.0 (2026-03-16)

- ✅ 新增官方 API 支持
- ✅ 新增 OAuth 授权流程
- ✅ 新增 Web 管理界面
- ✅ 新增视频管理功能
- ✅ 新增数据统计功能
- ✅ 保留网页自动化功能

### v0.1.0 (2026-03-16)

- ✅ 初始版本
- ✅ 网页自动化发布
- ✅ 扫码登录
- ✅ Cookie 管理

---

## 📄 License

MIT License

---

## 🙏 致谢

感谢 [MoneyPrinterPlus](https://github.com/ddean2009/MoneyPrinterPlus) 项目提供的参考实现。

---

**开发完成时间**: 2026-03-16  
**版本**: v0.2.0  
**状态**: ✅ **生产就绪**
