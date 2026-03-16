# 抖音一键发布工具

> 自动化抖音视频发布，支持扫码登录、一键发布、批量管理

[![Status](https://img.shields.io/badge/status-development-yellow)]()
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## ✨ 功能特性

### 已实现
- ✅ 扫码登录抖音
- ✅ Cookie 自动保存
- ✅ 视频上传
- ✅ 文案编辑
- ✅ 一键发布

### 计划中
- ⏳ 批量发布
- ⏳ 定时发布
- ⏳ 多账号管理
- ⏳ 发布队列

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. 登录抖音

```bash
python scripts/login.py
```

会打开浏览器，使用抖音 APP 扫码登录。

### 3. 发布视频

#### 方式一：命令行

```bash
python scripts/publish.py \
  --video ./videos/test.mp4 \
  --title "我的视频标题" \
  --desc "视频描述 #话题"
```

#### 方式二：Web 界面

```bash
python backend/main.py
```

然后访问 http://localhost:8000

#### 方式三：Python 代码

```python
from publisher.douyin_publisher import DouyinPublisher

publisher = DouyinPublisher()
publisher.publish(
    video_path="./videos/test.mp4",
    title="视频标题",
    description="视频描述 #话题"
)
```

## 📖 使用说明

### 登录

首次使用需要登录：

```bash
python scripts/login.py
```

1. 运行命令后会自动打开浏览器
2. 使用抖音 APP 扫描二维码
3. 登录成功后会自动保存 Cookie
4. 后续使用无需重复登录

### 发布视频

#### 基本发布

```bash
python scripts/publish.py \
  --video ./my_video.mp4 \
  --title "今天的好心情" \
  --desc "分享我的日常生活 #日常 #生活记录"
```

#### 带封面发布

```bash
python scripts/publish.py \
  --video ./my_video.mp4 \
  --cover ./cover.jpg \
  --title "绝美瞬间" \
  --desc "抓拍到的美景 #摄影 #美景"
```

#### 设置隐私

```bash
python scripts/publish.py \
  --video ./my_video.mp4 \
  --title "私密视频" \
  --privacy private  # public=公开，friend=好友可见，private=私密
```

### 检查登录状态

```bash
python scripts/check_login.py
```

### 退出登录

```bash
python scripts/logout.py
```

## 📁 项目结构

```
douyin-auto-publish/
├── backend/
│   ├── main.py              # FastAPI 服务
│   └── ...
├── publisher/
│   ├── douyin_publisher.py  # 发布器核心
│   └── ...
├── scripts/
│   ├── login.py             # 登录脚本
│   ├── publish.py           # 发布脚本
│   └── ...
├── storage/
│   ├── cookies/             # 登录状态
│   └── videos/              # 视频文件
├── requirements.txt
└── README.md
```

## ⚙️ 配置

### 环境变量

创建 `.env` 文件：

```bash
# 抖音配置
DOUYIN_PROFILE=default

# 服务配置
HOST=127.0.0.1
PORT=8000

# 存储路径
STORAGE_PATH=./storage
```

## ⚠️ 注意事项

1. **合规使用**：遵守抖音平台规则，不要发布违规内容
2. **发布频率**：建议每天发布 < 10 条，避免被判定为营销号
3. **账号安全**：妥善保管 Cookie 文件，不要泄露
4. **网络环境**：建议使用稳定的网络环境

## 🔧 故障排除

### 无法登录

- 检查网络连接
- 清除 Cookie 重新登录：`python scripts/logout.py`
- 更新 Playwright：`playwright install chromium`

### 发布失败

- 检查视频格式（支持 MP4、MOV 等）
- 检查视频大小（建议 < 500MB）
- 检查登录状态：`python scripts/check_login.py`

### 触发风控

- 降低发布频率
- 使用代理 IP
- 等待 24 小时后再试

## 📝 API 文档

启动服务后访问：http://localhost:8000/docs

### 主要接口

- `POST /api/login` - 登录抖音
- `POST /api/publish` - 发布视频
- `GET /api/status` - 检查登录状态
- `POST /api/logout` - 退出登录

## 🙏 致谢

本项目仅供学习研究使用，请勿用于违规用途。

---

**开发中** | 版本：0.1.0
