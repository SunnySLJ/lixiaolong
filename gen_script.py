import requests
import json
import sys

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

body = {
    "hot_topic": "春分遇上龙抬头，本世纪仅有 3 次的天文奇观",
    "platform": "douyin",
    "style": "viral",
    "tags": ["春分", "龙抬头", "传统习俗", "天文奇观", "二月二"]
}

response = requests.post("http://localhost:8899/api/zgf/gen-script", json=body, timeout=120)
result = response.json()

# 输出中文结果
print("=" * 60)
print("文案生成成功！")
print("=" * 60)
print(f"\n标题：{result.get('title', 'N/A')}")
print(f"视频类型：{result.get('video_type', 'N/A')}")
print(f"视频时长：{result.get('video_duration', 'N/A')}")
print(f"爆款指数：{result.get('viral_score', 'N/A')}/10")
print(f"适合平台：{', '.join(result.get('suitable_platforms', []))}")
print(f"BGM 风格：{result.get('bgm_style', 'N/A')}")
print(f"\n开场钩子 (Hook):")
print(f"   {result.get('hook', 'N/A')}")
print(f"\n完整脚本:")
print(f"   {result.get('full_script', 'N/A')}")
print(f"\n话题标签:")
for tag in result.get('hashtags', []):
    print(f"   {tag}")
print(f"\n制作建议:")
print(f"   {result.get('tips', 'N/A')}")
print(f"\n分镜脚本:")
for i, seg in enumerate(result.get('segments', []), 1):
    print(f"\n   镜头{i} ({seg.get('time', 'N/A')}):")
    print(f"   场景：{seg.get('scene', 'N/A')}")
    print(f"   字幕：{seg.get('text', 'N/A')}")
print("\n" + "=" * 60)
