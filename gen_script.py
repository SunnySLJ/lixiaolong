import requests
import json

# 简化参数
body = {
    "topic": "春分遇上龙抬头",
    "platform": "douyin"
}

response = requests.post("http://localhost:8899/api/zgf/gen-script", json=body, timeout=30)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
