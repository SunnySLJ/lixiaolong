# 抖音文案提取 Skill

根据抖音视频链接自动提取并生成爆款文案。

## 功能

- 支持抖音短链和长链
- 自动提取视频标题和描述
- 使用 AI 生成小红书/抖音风格文案
- 支持多种 AI 模型（Kimi、Claude、Gemini、GPT）

## 使用方法

### 方式一：直接调用

```python
from skills.douyin-extract.extractor import DouyinCopyExtractor

extractor = DouyinCopyExtractor()
result = await extractor.extract_copy("https://v.douyin.com/xxxxx/")
print(result['copy'])
```

### 方式二：命令行

```bash
python simple_extract.py "https://v.douyin.com/xxxxx/"
```

### 方式三：OpenClaw 中调用

在 OpenClaw 中直接使用：
```
提取这个抖音链接的文案：https://v.douyin.com/xxxxx/
```

## 配置

在 `backend/config/settings.json` 中配置 AI API：

```json
{
  "provider": "kimi",
  "apiKey": "your-api-key",
  "proxyUrl": ""
}
```

或使用环境变量：
```bash
export AI_PROVIDER=kimi
export AI_API_KEY=your-api-key
```

## 输出示例

```markdown
【爆款标题】
1. 🔥 这个技巧让我一天涨粉 1000+！
2. 99% 的人都不知道的抖音秘密...
3. 小白也能学会的爆款公式！

【正文】
家人们！今天一定要分享这个超实用的技巧！
...

【热门标签】
#抖音运营 #短视频创作 #自媒体 #爆款文案 #内容创作
```
