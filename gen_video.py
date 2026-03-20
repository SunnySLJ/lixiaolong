import requests
import json
import sys
import os

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

# 使用刚才生成的文案内容作为 prompt
prompt = "春分龙抬头天文奇观，漆黑夜空中春分与龙抬头天象重合，光芒四射，星辰变换，龙形光影与星辰交融，祥瑞之兆，神龙现身，天文望远镜探索宇宙奥秘"

# 输出目录
output_dir = "S:\\ruoyi\\video"
os.makedirs(output_dir, exist_ok=True)

# 使用配置中的服务商
body = {
    "prompt": prompt,
    "duration": 10,  # 测试用 10 秒
    "ratio": "9:16"
}

print("=" * 60)
print("正在调用视频生成接口...")
print("=" * 60)
print(f"提示词：{prompt}")
print(f"时长：{body['duration']}秒")
print(f"比例：{body['ratio']}")
print(f"输出目录：{output_dir}")
print("\n等待 AI 生成视频...\n")

try:
    response = requests.post(
        "http://localhost:8899/api/zgf/gen-video", 
        json=body, 
        timeout=180,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    
    print(f"HTTP 状态码：{response.status_code}")
    result = response.json()
    
    print("=" * 60)
    print("视频生成结果:")
    print("=" * 60)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("=" * 60)
    
    if result.get('task_id'):
        print(f"\n✓ 视频任务已提交！")
        print(f"任务 ID: {result.get('task_id')}")
        print(f"状态：{result.get('status')}")
        print(f"服务商：{result.get('provider')}")
        
        if result.get('video_url'):
            print(f"视频 URL: {result.get('video_url')}")
        else:
            print(f"\n视频正在生成中，请稍后查询状态...")
            print(f"可以使用任务 ID 查询：{result.get('task_id')}")
    elif result.get('error'):
        print(f"\n✗ 视频生成失败：{result.get('error')}")
        print("\n可能的原因：")
        print("1. AI 服务商 API 不可用（502/403/400 错误）")
        print("2. API Key 无效或余额不足")
        print("3. 提示词可能触发审核")
        print("\n建议：")
        print("- 检查 sora_config.json 中的 API Key 配置")
        print("- 尝试更换服务商（poloai/n1n/grsai/wuyin）")
        print("- 简化提示词内容")
    
except requests.exceptions.Timeout:
    print("请求超时！视频生成可能需要更长时间...")
except Exception as e:
    print(f"发生错误：{e}")
