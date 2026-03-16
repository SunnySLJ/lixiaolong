"""
抖音文案提取器 - OpenClaw Skill 版本
"""

import asyncio
import os
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any

# 添加 backend 目录到路径
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(SKILL_DIR, '..', '..', 'douyin-extract-modified', 'backend')
sys.path.insert(0, BACKEND_DIR)

import httpx
from openai import AsyncOpenAI
from google import genai


class DouyinCopyExtractor:
    """抖音文案提取器"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._load_config()
        self.output_dir = os.path.join(SKILL_DIR, 'outputs')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        config_file = os.path.join(BACKEND_DIR, 'config', 'settings.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            "provider": os.getenv("AI_PROVIDER", "kimi"),
            "apiKey": os.getenv("AI_API_KEY", ""),
            "proxyUrl": os.getenv("AI_PROXY_URL", "")
        }
    
    async def extract_copy(self, video_url: str, save: bool = True) -> Dict[str, Any]:
        """
        提取抖音文案
        
        Args:
            video_url: 抖音视频链接
            save: 是否保存到文件
            
        Returns:
            包含标题、描述、文案等信息的字典
        """
        from extractor_service import extract_video_data
        
        print(f"🚀 开始提取：{video_url}")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_dir = os.path.join(self.output_dir, timestamp)
        os.makedirs(task_dir, exist_ok=True)
        
        print("📥 正在提取视频数据...")
        video_data = await extract_video_data(video_url, task_dir)
        
        if not video_data:
            raise Exception("视频提取失败，请检查链接是否有效")
        
        print(f"✅ 视频提取成功：{video_data.get('title', '无标题')}")
        
        print("🤖 正在生成文案...")
        copy_result = await self._generate_copy(
            title=video_data.get('title', ''),
            description=video_data.get('description', ''),
            audio_path=video_data.get('local_audio_path', '')
        )
        
        result = {
            "timestamp": timestamp,
            "url": video_url,
            "title": video_data.get('title', ''),
            "description": video_data.get('description', ''),
            "copy": copy_result,
            "audio_path": video_data.get('local_audio_path', '')
        }
        
        if save:
            await self._save_result(result, task_dir)
        
        return result
    
    async def _generate_copy(self, title: str, description: str, audio_path: str = "") -> str:
        """使用 AI 生成文案"""
        provider = self.config.get("provider", "kimi")
        api_key = self.config.get("apiKey", "")
        proxy_url = self.config.get("proxyUrl", "")
        
        if not api_key:
            return "⚠️ API Key 未配置，请在 backend/config/settings.json 中配置"
        
        prompt = f"""
你是一个短视频爆款文案专家。请根据以下视频信息，撰写一篇吸引人的小红书/抖音文案。

【视频标题】：{title}
【视频描述】：{description}

任务要求：
1. 给出 5 个【爆款标题】，必须包含痛点或反差，带 Emoji
2. 撰写【正文】，结构清晰，分段落，第一句必须抓人眼球
3. 语气活泼，多用 Emoji，具有互动感
4. 结尾列出 10 个相关的【热门标签】(Hashtags)

请直接输出文案内容，不需要解释。
"""
        
        try:
            if provider == "kimi":
                return await self._call_kimi(prompt, api_key, proxy_url)
            elif provider == "claude":
                return await self._call_claude(prompt, api_key, proxy_url)
            elif provider == "gemini":
                return await self._call_gemini(prompt, api_key, proxy_url)
            elif provider in ["ppio", "openai"]:
                return await self._call_openai(prompt, api_key, proxy_url, provider)
            else:
                return f"⚠️ 不支持的 AI 厂商：{provider}"
                
        except Exception as e:
            return f"❌ 文案生成失败：{str(e)}"
    
    async def _call_kimi(self, prompt: str, api_key: str, proxy_url: str) -> str:
        """调用 Kimi API"""
        http_client = httpx.AsyncClient(proxy=proxy_url) if proxy_url else None
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1",
            http_client=http_client
        )
        
        completion = await client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return completion.choices[0].message.content
    
    async def _call_claude(self, prompt: str, api_key: str, proxy_url: str) -> str:
        """调用 Claude API"""
        http_client = httpx.AsyncClient(proxy=proxy_url) if proxy_url else None
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.anthropic.com/v1",
            http_client=http_client
        )
        
        completion = await client.chat.completions.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return completion.choices[0].message.content
    
    async def _call_gemini(self, prompt: str, api_key: str, proxy_url: str) -> str:
        """调用 Gemini API"""
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )
        return response.text
    
    async def _call_openai(self, prompt: str, api_key: str, proxy_url: str, provider: str) -> str:
        """调用 OpenAI 或兼容 API"""
        http_client = httpx.AsyncClient(proxy=proxy_url) if proxy_url else None
        base_url = "https://api.ppio.com/openai" if provider == "ppio" else "https://api.openai.com/v1"
        model = "qwen/qwen3.5-27b" if provider == "ppio" else "gpt-3.5-turbo"
        
        client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            http_client=http_client
        )
        
        completion = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        
        return completion.choices[0].message.content
    
    async def _save_result(self, result: Dict[str, Any], task_dir: str):
        """保存结果到文件"""
        copy_file = os.path.join(task_dir, "copy.txt")
        with open(copy_file, 'w', encoding='utf-8') as f:
            f.write(f"视频链接：{result['url']}\n")
            f.write(f"标题：{result['title']}\n")
            f.write(f"描述：{result['description']}\n\n")
            f.write("=" * 50 + "\n\n")
            f.write(result['copy'])
        
        json_file = os.path.join(task_dir, "result.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"💾 结果已保存至：{task_dir}")


async def extract_douyin_copy(video_url: str) -> str:
    """
    OpenClaw Skill 入口函数
    
    Args:
        video_url: 抖音视频链接
        
    Returns:
        生成的文案
    """
    extractor = DouyinCopyExtractor()
    result = await extractor.extract_copy(video_url)
    return result['copy']
