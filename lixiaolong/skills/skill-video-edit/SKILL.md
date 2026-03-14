# skill-video-edit

视频混剪 Skill - 自动化视频制作

## 功能描述

基于 FFmpeg 实现自动化视频剪辑、拼接、添加字幕和背景音乐。

## 核心功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 视频拼接 | ✅ | 多个视频片段无缝拼接 |
| 转场效果 | ✅ | 淡入淡出等转场 |
| 字幕合成 | ✅ | 添加文字字幕 |
| BGM 混音 | ✅ | 添加背景音乐 |
| 封面生成 | ✅ | 自动提取封面 |
| 视频裁剪 | ✅ | 按时间裁剪 |
| 尺寸调整 | ✅ | 适配不同平台 |

## 输入参数

```json
{
  "clips": [
    {
      "path": "video1.mp4",
      "startTime": "00:00:00",
      "duration": 10
    }
  ],
  "bgm": "bgm.mp3",
  "subtitles": [
    {
      "text": "字幕内容",
      "startTime": "00:00:00",
      "duration": 5
    }
  ],
  "outputPath": "output/final.mp4",
  "options": {
    "fontSize": 24,
    "fontColor": "white",
    "width": 1080,
    "height": 1920
  }
}
```

## 使用示例

### OpenClaw 调用

```bash
openclaw skill run skill-video-edit --params '{
  "clips": [{"path": "clip1.mp4", "duration": 10}],
  "bgm": "bgm.mp3",
  "outputPath": "output/video.mp4"
}'
```

### 程序化调用

```javascript
const videoEdit = require('./skills/skill-video-edit');

const result = await videoEdit.main({
  clips: [
    { path: 'clip1.mp4', startTime: '0', duration: 10 },
    { path: 'clip2.mp4', startTime: '0', duration: 15 }
  ],
  bgm: 'bgm.mp3',
  subtitles: [
    { text: '精彩瞬间', startTime: '0', duration: 5 }
  ],
  outputPath: 'output/final.mp4'
});

console.log(result);
// {
//   success: true,
//   videoPath: 'output/final.mp4',
//   coverPath: 'output/final_cover.jpg',
//   duration: 25
// }
```

## 输出格式

```json
{
  "success": true,
  "videoPath": "output/final.mp4",
  "coverPath": "output/final_cover.jpg",
  "duration": 25,
  "timestamp": "2026-03-14T14:30:00Z"
}
```

## 环境要求

### 必需
- Node.js >= 14
- FFmpeg

### 可选
- FFMPEG_PATH 环境变量（自定义 FFmpeg 路径）

## 安装 FFmpeg

### Windows
```bash
# 使用 Scoop
scoop install ffmpeg

# 或下载安装包
# https://ffmpeg.org/download.html
```

### macOS
```bash
brew install ffmpeg
```

### Linux
```bash
sudo apt-get install ffmpeg
```

## API 参考

### createVideo(params)

完整视频制作流程。

**参数：**
- `clips` - 视频片段数组
- `bgm` - 背景音乐路径
- `subtitles` - 字幕数组
- `outputPath` - 输出路径
- `options` - 其他选项

**返回：** 制作结果

### concatVideos(videoFiles, outputPath)

拼接多个视频文件。

### addSubtitle(inputPath, outputPath, text, options)

添加文字字幕。

### addBGM(videoPath, bgmPath, outputPath, volume)

添加背景音乐。

### generateCover(videoPath, outputPath, timestamp)

生成视频封面。

### trimVideo(inputPath, outputPath, startTime, duration)

裁剪视频片段。

## 最佳实践

### 1. 视频格式统一

确保所有输入视频格式一致：
- 分辨率：1080x1920（抖音/小红书）
- 帧率：30fps
- 编码：H.264

### 2. BGM 音量控制

背景音乐音量建议：
- 人声视频：0.2-0.3
- 纯音乐视频：0.5-0.6

### 3. 字幕位置

- 底部：安全区域，不遮挡主要内容
- 字体大小：24-32px
- 颜色：白色 + 黑色描边

### 4. 封面选择

- 选择视频中最精彩的帧
- 时间戳建议：00:00:01-00:00:03
- 分辨率：1080x1920

## 故障排查

### FFmpeg 未找到

**错误：** `FFmpeg 未安装或未找到`

**解决：**
```bash
# 检查是否安装
ffmpeg -version

# 设置环境变量
set FFMPEG_PATH=C:\path\to\ffmpeg.exe
```

### 视频拼接失败

**可能原因：**
- 视频格式不一致
- 编码不兼容

**解决：**
- 统一视频格式
- 先转码再拼接

### 字幕乱码

**解决：**
- 确保字幕文本为 UTF-8 编码
- 使用英文或转义特殊字符

## 待办事项

- [ ] 支持 .srt 字幕文件
- [ ] 添加更多转场效果
- [ ] 视频滤镜（美颜、滤镜）
- [ ] 批量处理
- [ ] 进度回调
- [ ] 视频压缩优化

## 相关文件

- `index.js` - 主逻辑代码
- `package.json` - 依赖配置
- `test.js` - 测试脚本

## 更新日志

### v1.0.0 (2026-03-14)
- ✅ 初始版本
- ✅ 视频拼接
- ✅ 字幕合成
- ✅ BGM 混音
- ✅ 封面生成
- ✅ 视频裁剪

---

**作者：** 帧龙虾团队  
**版本：** 1.0.0  
**最后更新：** 2026-03-14
