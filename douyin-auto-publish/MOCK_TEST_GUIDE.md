# 🧪 抖音 API Mock 测试指南

**无需真实 API Key，立即测试完整流程！**

---

## 🚀 快速开始

### 1. 启动 Mock 服务器

```bash
cd C:\Users\爽爽\.openclaw\workspace\douyin-auto-publish

# 启动 Mock 服务器
python mock_server.py
```

**服务器会显示**:
```
============================================================
抖音 API Mock 测试服务器
============================================================

测试凭证:
  client_key: test_client_key
  client_secret: test_client_secret

API 文档:
  http://localhost:8000/docs

健康检查:
  http://localhost:8000/health
============================================================
```

### 2. 运行测试脚本

打开新的命令行窗口：

```bash
python test_mock_api.py
```

**测试流程**:
1. ✅ 初始化客户端
2. ✅ 生成 OAuth URL
3. ✅ 获取 access_token
4. ✅ 上传视频（模拟）
5. ✅ 发布视频
6. ✅ 获取视频列表
7. ✅ 获取视频数据

---

## 📝 手动测试 API

### 访问 API 文档

浏览器打开：http://localhost:8000/docs

可以看到所有 API 端点的交互式文档。

### 测试 OAuth 授权

**1. 获取授权 URL**

```bash
curl "http://localhost:8000/oauth/authorize?client_key=test_client_key&redirect_uri=http://localhost:8000/callback&scope=user_info,video.create,video.upload&response_type=code&state=test123"
```

**响应**:
```json
{
  "message": "请在浏览器中打开以下链接完成授权",
  "authorize_url": "http://localhost:8000/callback?code=xxx&state=test123",
  "mock_code": "abc123..."
}
```

**2. 获取 access_token**

```bash
curl "http://localhost:8000/oauth/access_token/?client_key=test_client_key&client_secret=test_client_secret&code=abc123&grant_type=authorization_code&redirect_uri=http://localhost:8000/callback"
```

**响应**:
```json
{
  "error_code": 0,
  "description": "Success",
  "data": {
    "access_token": "xxx",
    "refresh_token": "yyy",
    "expires_in": 7200
  }
}
```

### 测试视频上传

```bash
curl -X POST "http://localhost:8000/api/douyin/v1/video/upload_video/?access_token=YOUR_TOKEN&title=测试视频"
```

**响应**:
```json
{
  "error_code": 0,
  "description": "Success",
  "data": {
    "video_id": "video_1234567890",
    "title": "测试视频",
    "upload_time": 1234567890
  }
}
```

### 测试视频发布

```bash
curl -X POST "http://localhost:8000/api/douyin/v1/video/create/" \
  -H "Content-Type: application/json" \
  -d '{"access_token":"YOUR_TOKEN","video_id":"video_123","text":"视频标题 #话题"}'
```

---

## 💻 Python 代码测试

### 使用 douyin_openapi 客户端

```python
from douyin_openapi import DouyinOpenAPI

# 初始化
client = DouyinOpenAPI(
    client_key="test_client_key",
    client_secret="test_client_secret"
)

# 获取 OAuth URL
oauth_url = client.get_oauth_url("http://localhost:8000/callback")
print(f"OAuth URL: {oauth_url}")

# 模拟授权（实际使用需要用户扫码）
mock_code = "test_code_123"

# 获取 access_token
result = client.get_access_token(mock_code, "http://localhost:8000/callback")

if result.get("error_code") == 0:
    print(f"Access Token: {client.access_token}")
    
    # 上传视频
    upload_result = client.upload_video("./video.mp4", "测试视频")
    video_id = upload_result.get("data", {}).get("video_id")
    
    # 发布视频
    publish_result = client.create_video(video_id, "视频标题 #话题")
    
    # 获取视频列表
    videos = client.list_videos(count=10)
    
    # 获取视频数据
    data = client.get_video_data(video_id)
```

---

## 🎯 Mock 服务器功能

### 支持的接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/oauth/authorize` | GET | OAuth 授权 |
| `/oauth/access_token/` | GET | 获取 access_token |
| `/oauth/refresh_token/` | GET | 刷新 token |
| `/api/douyin/v1/video/upload_video/` | POST | 上传视频 |
| `/api/douyin/v1/video/create/` | POST | 发布视频 |
| `/api/douyin/v1/video/list/` | GET | 视频列表 |
| `/api/douyin/v1/video/delete/` | POST | 删除视频 |
| `/api/douyin/v1/video/data/` | GET | 视频数据 |

### Mock 数据

- **Videos**: 存储在内存中，服务器重启后清空
- **Tokens**: 有效期 2 小时
- **统计数据**: 随机生成（播放量、点赞等）

---

## ⚠️ 注意事项

### Mock vs 真实 API

| 特性 | Mock 服务器 | 真实 API |
|------|------------|----------|
| 文件上传 | ❌ 模拟 | ✅ 真实上传 |
| OAuth 授权 | ❌ 模拟 | ✅ 需要扫码 |
| 视频发布 | ❌ 模拟 | ✅ 真实发布 |
| 数据存储 | ❌ 内存 | ✅ 抖音服务器 |
| Token 验证 | ✅ 简单验证 | ✅ 严格验证 |
| 错误处理 | ⚠️ 简化 | ✅ 完整 |

### 使用建议

**Mock 服务器适合**:
- ✅ 测试代码逻辑
- ✅ 学习 API 调用
- ✅ 开发调试
- ✅ 演示功能

**真实 API 适合**:
- ✅ 实际发布视频
- ✅ 生产管理
- ✅ 数据获取

---

## 🔄 切换到真实 API

当你获得真实的 API Key 后：

**1. 修改配置**

```python
# 使用真实 API
client = DouyinOpenAPI(
    client_key="你的真实 client_key",
    client_secret="你的真实 client_secret"
)

# 或者修改配置文件 config.json
```

**2. 修改服务器地址**

```python
# 在 douyin_openapi.py 中修改
self.base_url = "https://open.douyin.com"
self.oauth_url = "https://open.douyin.com/oauth"
```

**3. 重新测试**

```bash
python test_mock_api.py  # 会自动使用真实 API
```

---

## 📚 完整测试流程

### 步骤 1: 启动 Mock 服务器

```bash
python mock_server.py
```

### 步骤 2: 运行测试脚本

```bash
python test_mock_api.py
```

### 步骤 3: 查看测试结果

```
============================================================
抖音 API Mock 测试
============================================================

1. 初始化客户端...
✅ 客户端初始化成功

2. 获取 OAuth 授权 URL...
✅ OAuth URL 生成成功

3. 模拟授权获取 code...
   Code: test_auth_code_123456

4. 获取 access_token...
✅ Access Token: abc123...
   Expires In: 7200s

5. 上传视频（模拟）...
✅ 上传成功，video_id: video_1234567890

6. 发布视频...
✅ 发布成功！

7. 获取视频列表...
✅ 获取到 1 个视频
   - 测试视频 (video_1234567890)

8. 获取视频数据（模拟）...
✅ 视频数据:
   播放量：5432
   点赞数：234
   评论数：45

============================================================
✅ Mock 测试完成！
============================================================
```

---

## 🎉 总结

**Mock 服务器让你**:
- ✅ 无需等待 API 审核
- ✅ 无需企业资质
- ✅ 立即开始测试
- ✅ 熟悉 API 流程
- ✅ 验证代码逻辑

**下一步**:
1. 启动 Mock 服务器
2. 运行测试脚本
3. 熟悉 API 调用
4. 等待真实 API Key
5. 切换到生产环境

---

**开始测试吧！** 🚀

```bash
python mock_server.py
```
