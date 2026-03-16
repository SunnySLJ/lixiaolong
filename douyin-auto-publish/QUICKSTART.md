# 快速开始指南

## 5 分钟上手抖音一键发布工具

### 第 1 步：安装依赖（2 分钟）

```bash
# 进入项目目录
cd douyin-auto-publish

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 第 2 步：登录抖音（1 分钟）

```bash
python scripts/login.py
```

运行后会：
1. 自动打开浏览器
2. 显示抖音登录二维码
3. 使用抖音 APP 扫码
4. 登录成功后自动保存 Cookie

### 第 3 步：发布视频（1 分钟）

准备一个测试视频（MP4 格式），然后运行：

```bash
python scripts/publish.py \
  --video ./test_video.mp4 \
  --title "我的第一个自动发布视频" \
  --desc "使用抖音一键发布工具发布的 #AI #自动化"
```

就这么简单！🎉

---

## 常用命令

### 检查登录状态

```bash
python scripts/publish.py --check-login
```

### 查看帮助

```bash
python scripts/publish.py --help
```

### 使用不同的账号

```bash
# 登录新账号
python scripts/login.py --profile account2

# 使用指定账号发布
python scripts/publish.py --video ./test.mp4 --title "视频" --profile account2
```

### 私密发布

```bash
python scripts/publish.py \
  --video ./test.mp4 \
  --title "私密视频" \
  --privacy private
```

---

## 完整示例

### 示例 1：发布日常视频

```bash
python scripts/publish.py \
  -v "./videos/daily_life.mp4" \
  -t "今天的好心情 ☀️" \
  -d "记录美好生活 #日常 #生活记录 #vlog"
```

### 示例 2：发布教程视频

```bash
python scripts/publish.py \
  -v "./videos/tutorial.mp4" \
  -t "3 分钟学会 XXX 技巧" \
  -d "超实用的 XXX 教程，建议收藏！#教程 #技巧 #干货" \
  -p public
```

### 示例 3：批量发布（脚本）

创建 `batch_publish.py`：

```python
import asyncio
from publisher.douyin_publisher import DouyinPublisher

async def batch_publish():
    publisher = DouyinPublisher()
    
    videos = [
        {
            "path": "./videos/video1.mp4",
            "title": "视频 1 标题",
            "desc": "视频 1 描述 #话题"
        },
        {
            "path": "./videos/video2.mp4",
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
        await asyncio.sleep(5)  # 避免频繁操作

asyncio.run(batch_publish())
```

---

## 常见问题

### Q: 登录时浏览器打不开？

A: 确保安装了 Chrome 浏览器，或者运行：
```bash
playwright install chromium
```

### Q: 发布失败怎么办？

A: 
1. 检查登录状态：`python scripts/publish.py --check-login`
2. 重新登录：`python scripts/login.py`
3. 检查视频格式（支持 MP4、MOV 等）
4. 检查视频大小（建议 < 500MB）

### Q: Cookie 保存在哪里？

A: `./storage/cookies/` 目录下

### Q: 如何切换账号？

A: 使用 `--profile` 参数：
```bash
python scripts/login.py --profile account2
python scripts/publish.py --video ./test.mp4 --profile account2
```

### Q: 可以定时发布吗？

A: 当前版本不支持，计划中。可以使用系统定时任务：

Windows（任务计划程序）：
```bash
schtasks /create /tn "DouyinPublish" /tr "python scripts/publish.py -v ./video.mp4 -t 标题" /sc daily /st 09:00
```

Linux（cron）：
```bash
crontab -e
# 添加：0 9 * * * cd /path/to/project && python scripts/publish.py -v ./video.mp4 -t 标题
```

---

## 下一步

- 📖 查看完整文档：`README.md`
- 🔧 高级配置：`.env.example`
- 💻 API 文档：启动 Web 服务后访问 `/docs`

祝你使用愉快！🎉
