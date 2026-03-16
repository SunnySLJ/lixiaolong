# 🎬 抖音视频上传测试

**测试视频**: `storage/videos/test.mp4` (14.95 MB) ✅

---

## 🚀 快速测试（3 步）

### 第 1 步：登录抖音

```bash
cd C:\Users\爽爽\.openclaw\workspace\douyin-auto-publish

python scripts/quick_login.py
```

**会发生什么**：
1. ✅ 自动打开 Chrome 浏览器
2. ✅ 显示抖音登录二维码
3. ✅ 使用抖音 APP 扫码
4. ✅ 自动保存 Cookie
5. ✅ 浏览器自动关闭

---

### 第 2 步：上传视频

```bash
python scripts/publish.py \
  --video ./storage/videos/test.mp4 \
  --title "AI 自动化测试视频" \
  --desc "使用抖音发布工具自动上传 #AI #自动化 #科技前沿"
```

**参数说明**：
- `--video`: 视频文件路径
- `--title`: 视频标题
- `--desc`: 视频描述（包含话题标签）

**可选参数**：
- `--privacy`: 隐私设置（public/friend/private）
- `--profile`: 使用的账号配置（支持多账号）

---

### 第 3 步：查看结果

发布成功后，打开抖音 APP 查看：
- 我的作品
- 视频标题：AI 自动化测试视频
- 描述：使用抖音发布工具自动上传 #AI #自动化 #科技前沿

---

## 📝 完整测试流程

### 测试 1：检查登录状态

```bash
python scripts/publish.py --check-login
```

**预期输出**：
```
✅ 已登录
Cookie 文件：storage/cookies/default.json
```

---

### 测试 2：登录抖音

```bash
python scripts/quick_login.py
```

**输出示例**：
```
============================================================
抖音登录 - 自动化模式
============================================================

即将打开浏览器...
请使用抖音 APP 扫描二维码登录
登录成功后会自动关闭浏览器并保存 Cookie

============================================================
登录成功！Cookie 已保存

下一步：发布视频
命令：python scripts/publish.py -v ./video.mp4 -t "标题" -d "描述"
============================================================
```

---

### 测试 3：发布视频

```bash
python scripts/publish.py \
  -v ./storage/videos/test.mp4 \
  -t "AI 自动化测试视频" \
  -d "使用抖音发布工具自动上传 #AI #自动化 #科技前沿"
```

**输出示例**：
```
============================================================
抖音发布工具 - 发布视频
============================================================

视频：./storage/videos/test.mp4
标题：AI 自动化测试视频
描述：使用抖音发布工具自动上传 #AI #自动化 #科技前沿
隐私：public
配置：default

✅ 登录状态正常

🚀 开始发布...
正在启动浏览器...
正在打开上传页面...
正在上传视频...
✓ 视频文件已选择
等待视频上传完成...
正在设置标题...
✓ 标题已设置
正在设置描述...
✓ 描述已设置
正在查找发布按钮...
✓ 找到发布按钮，点击发布...
等待发布完成...
✅ 视频发布成功！

============================================================
🎉 发布成功！
============================================================
```

---

### 测试 4：验证发布

打开抖音 APP：
1. 点击"我"
2. 查看"作品"
3. 找到最新视频
4. 确认标题和描述

---

## ⚙️ 高级用法

### 批量发布

创建 `batch_publish.py`：

```python
import asyncio
from publisher.douyin_publisher import DouyinPublisher

async def batch_publish():
    publisher = DouyinPublisher()
    
    videos = [
        {
            "path": "./storage/videos/video1.mp4",
            "title": "视频 1 标题",
            "desc": "视频 1 描述 #话题"
        },
        {
            "path": "./storage/videos/video2.mp4",
            "title": "视频 2 标题",
            "desc": "视频 2 描述 #话题"
        },
    ]
    
    for video in videos:
        result = await publisher.publish(
            video_path=video["path"],
            title=video["title"],
            description=video["desc"]
        )
        print(f"发布结果：{result}")
        await asyncio.sleep(60)  # 避免频繁操作

asyncio.run(batch_publish())
```

---

### 定时发布

使用系统定时任务：

#### Windows 任务计划程序

```bash
schtasks /create /tn "DouyinPublish" /tr "python C:\Users\爽爽\.openclaw\workspace\douyin-auto-publish\scripts\publish.py -v ./video.mp4 -t 标题" /sc daily /st 09:00
```

#### Linux Cron

```bash
crontab -e
# 添加：0 9 * * * cd /path/to/project && python scripts/publish.py -v ./video.mp4 -t 标题
```

---

### 多账号发布

```bash
# 登录多个账号
python scripts/quick_login.py --profile account1
python scripts/quick_login.py --profile account2

# 使用指定账号发布
python scripts/publish.py \
  -v ./video.mp4 \
  -t "标题" \
  --profile account2
```

---

## 📊 测试清单

- [ ] 准备测试视频 (14.95 MB ✅)
- [ ] 登录抖音
- [ ] 检查登录状态
- [ ] 上传视频
- [ ] 设置标题和描述
- [ ] 点击发布
- [ ] 等待发布完成
- [ ] 在抖音 APP 中验证

---

## ⚠️ 注意事项

### 视频要求

- ✅ 格式：MP4
- ✅ 大小：14.95 MB (< 4GB ✅)
- ✅ 时长：< 15 分钟
- ✅ 分辨率：720p 及以上

### 发布限制

- 每天发布 < 10 条（避免被判定为营销号）
- 两条视频间隔 > 5 分钟
- 不要使用违规内容

### 账号安全

- 使用真实网络环境
- 不要使用代理
- 定期更新登录状态
- 建议使用小号测试

---

## 🔧 故障排除

### 问题 1：无法登录

**解决**：
```bash
# 清除旧 Cookie
rm -rf storage/cookies/*

# 重新登录
python scripts/quick_login.py
```

### 问题 2：上传失败

**可能原因**：
- Cookie 过期
- 视频格式不支持
- 网络问题

**解决**：
```bash
# 重新登录
python scripts/quick_login.py

# 检查视频格式
# 确保是 MP4 格式

# 检查网络连接
```

### 问题 3：发布按钮找不到

**可能原因**：
- 页面结构变化
- 登录状态失效

**解决**：
```bash
# 重新登录
python scripts/quick_login.py

# 查看调试截图
# debug_*.png 文件
```

---

## 📁 相关文件

| 文件 | 说明 |
|------|------|
| `scripts/quick_login.py` | 快速登录脚本 |
| `scripts/publish.py` | 发布脚本 |
| `publisher/douyin_publisher.py` | 发布器核心 |
| `storage/cookies/default.json` | Cookie 文件 |
| `storage/videos/test.mp4` | 测试视频 |

---

## 🎯 快速命令

```bash
# 1. 登录
python scripts/quick_login.py

# 2. 检查登录
python scripts/publish.py --check-login

# 3. 发布视频
python scripts/publish.py \
  -v ./storage/videos/test.mp4 \
  -t "AI 自动化测试视频" \
  -d "#AI #自动化 #科技"

# 4. 查看帮助
python scripts/publish.py --help
```

---

## 🎉 开始测试

**视频已准备**：`storage/videos/test.mp4` (14.95 MB)

**现在运行**：
```bash
python scripts/quick_login.py  # 登录
python scripts/publish.py -v ./storage/videos/test.mp4 -t "AI 自动化测试视频" -d "#AI #自动化"
```

**然后在抖音 APP 中查看发布的视频！** 📱
