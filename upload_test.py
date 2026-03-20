#!/usr/bin/env python3
"""Upload video to Douyin using browser tool's CDP"""
import sys
from pathlib import Path

video_path = r"C:\Users\爽爽\Desktop\图片\2.mp4"
title = "春日随拍小片段｜城市日常记录"
desc = "今天随手记录一段生活片段，节奏轻松，画面干净，适合当作日常更新。"
tags = ["日常记录", "生活碎片", "随拍", "vlog"]

print(f"视频路径：{video_path}")
print(f"标题：{title}")
print(f"描述：{desc}")
print(f"标签：{', '.join(tags)}")
print("\n请手动点击上传按钮并选择文件，或使用以下命令：")
print(f"python scripts/douyin_upload.py --video \"{video_path}\" --title \"{title}\" --desc \"{desc}\" --tags {' '.join(tags)}")
