"""
Browser Use API Key 配置工具
"""

import os
from pathlib import Path

def configure_api_key():
    print("=" * 60)
    print("🔑 Browser Use API Key 配置工具")
    print("=" * 60)
    print()
    
    # 获取 API Key
    api_key = input("请输入您的 Browser Use API Key (bu_xxx): ").strip()
    
    if not api_key.startswith('bu_'):
        print("❌ 错误：API Key 应该以 'bu_' 开头")
        return False
    
    # 创建 .env 文件
    env_path = Path(__file__).parent / '.env'
    
    env_content = f"""# Browser Use Cloud API Key
BROWSER_USE_API_KEY={api_key}

# 可选：其他 LLM 配置
# GOOGLE_API_KEY=
# ANTHROPIC_API_KEY=

# 可选：Browser Use 配置
# BROWSER_USE_CLOUD=true
# BROWSER_USE_HEADLESS=false
"""
    
    try:
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print()
        print("=" * 60)
        print("✅ API Key 配置成功！")
        print("=" * 60)
        print()
        print(f"配置文件：{env_path}")
        print()
        print("下一步：")
        print("1. 运行测试脚本验证配置")
        print("   uv run python test_browser_use.py")
        print()
        print("2. 查看集成文档")
        print("   INTEGRATION.md")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ 配置失败：{e}")
        return False

if __name__ == "__main__":
    configure_api_key()
