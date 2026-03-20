import sys
sys.stdout.reconfigure(encoding='utf-8')

import argparse
import subprocess

video_path = r"S:\ruoyi\video\春分龙抬头_20260320113103A039.mp4"
title = "春分龙抬头天文奇观✨本世纪仅 3 次"
desc = "春分遇上龙抬头，百年难遇的天文奇观！漆黑夜空中星辰变换，龙形光影与星辰交融，祥瑞之兆。#春分龙抬头 #天文奇观 #百年难遇 #祥瑞之兆 #视觉盛宴"
tags = ["春分龙抬头", "天文奇观", "百年难遇", "祥瑞之兆", "视觉盛宴"]

cmd = [
    "python",
    r"C:\Users\爽爽\.openclaw\workspace\skills\douyin-video-upload\scripts\douyin_upload.py",
    "--video", video_path,
    "--title", title,
    "--desc", desc,
    "--tags"
] + tags + ["--publish"]

print("=" * 60)
print("抖音视频上传")
print("=" * 60)
print(f"视频：{video_path}")
print(f"标题：{title}")
print(f"描述：{desc[:50]}...")
print(f"标签：{', '.join(tags)}")
print("=" * 60)

result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
print(result.stdout)
if result.stderr:
    print(result.stderr)
