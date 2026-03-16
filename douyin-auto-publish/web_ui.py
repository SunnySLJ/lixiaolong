"""
抖音发布工具 - Web 管理界面

支持：
1. 官方 API 配置和 OAuth 授权
2. 网页自动化配置
3. 视频上传和发布
4. 发布任务管理
5. 数据统计

运行：streamlit run web_ui.py
"""

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
import sys

# 添加项目路径
sys.path.insert(0, '.')
from douyin_openapi import DouyinOpenAPI

# 页面配置
st.set_page_config(
    page_title="抖音发布工具",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 session state
if 'client' not in st.session_state:
    st.session_state.client = None
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'config' not in st.session_state:
    st.session_state.config = {}

# 加载配置
def load_config():
    config_path = Path("config.json")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_config(config):
    config_path = Path("config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

# 侧边栏
st.sidebar.title("🎬 抖音发布工具")
st.sidebar.markdown("---")

# 页面选择
page = st.sidebar.radio(
    "选择功能",
    ["📋 控制台", "⚙️ 官方 API 配置", "🤖 网页自动化", "📹 发布视频", "📊 视频管理"]
)

st.sidebar.markdown("---")
st.sidebar.info("版本：v0.2.0\n\n支持：官方 API + 网页自动化")

# ==================== 控制台 ====================
if page == "📋 控制台":
    st.title("📋 控制台")
    
    # 加载配置
    config = load_config()
    st.session_state.config = config
    
    # 状态概览
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="官方 API 状态",
            value="✅ 已配置" if config.get("douyin_openapi", {}).get("client_key") else "❌ 未配置",
            delta=None
        )
    
    with col2:
        st.metric(
            label="网页自动化",
            value="✅ 可用" if config.get("web_automation", {}).get("enabled") else "❌ 禁用",
            delta=None
        )
    
    with col3:
        st.metric(
            label="Access Token",
            value="✅ 有效" if st.session_state.access_token else "❌ 无效",
            delta=None
        )
    
    with col4:
        # 统计视频数量
        videos_path = config.get("storage", {}).get("videos_path", "./storage/videos")
        video_count = len(list(Path(videos_path).glob("*.mp4"))) if Path(videos_path).exists() else 0
        st.metric(
            label="待发布视频",
            value=video_count,
            delta=None
        )
    
    st.markdown("---")
    
    # 快速操作
    st.subheader("⚡ 快速操作")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔑 开始 OAuth 授权", use_container_width=True):
            if config.get("douyin_openapi", {}).get("client_key"):
                client = DouyinOpenAPI(
                    config["douyin_openapi"]["client_key"],
                    config["douyin_openapi"]["client_secret"]
                )
                oauth_url = client.get_oauth_url(config["douyin_openapi"]["redirect_uri"])
                st.markdown(f"**请在浏览器打开以下链接进行授权：**")
                st.code(oauth_url)
                st.info("授权完成后，将返回的 code 填入下方输入框")
                
                code = st.text_input("授权码")
                if st.button("确认授权"):
                    if code:
                        result = client.get_access_token(code, config["douyin_openapi"]["redirect_uri"])
                        if result.get("error_code") == 0:
                            st.success("✅ 授权成功！")
                            st.session_state.access_token = client.access_token
                            # 保存 token 到配置
                            config["douyin_openapi"]["access_token"] = client.access_token
                            config["douyin_openapi"]["refresh_token"] = client.refresh_token
                            config["douyin_openapi"]["token_expires_at"] = client.token_expires_at
                            save_config(config)
                        else:
                            st.error(f"❌ 授权失败：{result.get('description', '未知错误')}")
            else:
                st.error("请先在【官方 API 配置】页面配置 client_key 和 client_secret")
    
    with col2:
        if st.button("📹 上传视频", use_container_width=True):
            st.switch_page("pages/03_📹_发布视频.py")
    
    # 最近发布记录
    st.markdown("---")
    st.subheader("📝 最近发布记录")
    
    logs_path = Path(config.get("storage", {}).get("logs_path", "./logs"))
    if logs_path.exists():
        log_files = sorted(logs_path.glob("*.log"), key=os.path.getmtime, reverse=True)[:5]
        if log_files:
            for log_file in log_files:
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    st.text_area(
                        f"📄 {log_file.name}",
                        content[:500] + "..." if len(content) > 500 else content,
                        height=100,
                        disabled=True
                    )
        else:
            st.info("暂无发布记录")
    else:
        st.info("日志目录不存在")

# ==================== 官方 API 配置 ====================
elif page == "⚙️ 官方 API 配置":
    st.title("⚙️ 官方 API 配置")
    
    st.markdown("""
    ### 📋 配置说明
    
    使用抖音官方 API 需要先在 [抖音开放平台](https://open.douyin.com/) 创建应用并获取资质。
    
    **申请流程：**
    1. 注册企业账号并完成认证
    2. 创建应用
    3. 提交资质审核（1-2 周）
    4. 审核通过后获取 `client_key` 和 `client_secret`
    
    **官方文档：**
    - [抖音内容发布方案](https://open.douyin.com/platform/resource/docs/ability/content-management/douyin-publish-solution/)
    - [上传视频接口](https://open.douyin.com/api/douyin/v1/video/upload_video/)
    - [发布视频接口](https://open.douyin.com/api/douyin/v1/video/create/)
    """)
    
    st.markdown("---")
    
    # 加载当前配置
    config = load_config()
    api_config = config.get("douyin_openapi", {})
    
    # 配置表单
    col1, col2 = st.columns(2)
    
    with col1:
        client_key = st.text_input(
            "Client Key",
            value=api_config.get("client_key", ""),
            help="从抖音开放平台获取的 client_key"
        )
        
        client_secret = st.text_input(
            "Client Secret",
            value=api_config.get("client_secret", ""),
            help="从抖音开放平台获取的 client_secret",
            type="password"
        )
    
    with col2:
        redirect_uri = st.text_input(
            "授权回调地址",
            value=api_config.get("redirect_uri", "http://localhost:8000/callback"),
            help="OAuth 授权回调地址"
        )
        
        enabled = st.checkbox(
            "启用官方 API",
            value=api_config.get("enabled", False)
        )
    
    # Access Token 信息（只读）
    st.markdown("---")
    st.subheader("🔑 Token 信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input(
            "Access Token",
            value=api_config.get("access_token", ""),
            disabled=True,
            help="当前有效的 access_token"
        )
    
    with col2:
        expires_at = api_config.get("token_expires_at", 0)
        if expires_at > 0:
            expires_str = datetime.fromtimestamp(expires_at).strftime("%Y-%m-%d %H:%M:%S")
            st.text_input(
                "Token 过期时间",
                value=expires_str,
                disabled=True
            )
        else:
            st.text_input(
                "Token 过期时间",
                value="未获取",
                disabled=True
            )
    
    # 保存按钮
    st.markdown("---")
    if st.button("💾 保存配置", type="primary", use_container_width=True):
        config["douyin_openapi"] = {
            "enabled": enabled,
            "client_key": client_key,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "access_token": api_config.get("access_token", ""),
            "refresh_token": api_config.get("refresh_token", ""),
            "token_expires_at": api_config.get("token_expires_at", 0)
        }
        save_config(config)
        st.success("✅ 配置已保存！")
        st.session_state.config = config
        
        # 初始化客户端
        if client_key and client_secret:
            st.session_state.client = DouyinOpenAPI(client_key, client_secret)
            st.info("✅ 客户端已初始化")

# ==================== 网页自动化 ====================
elif page == "🤖 网页自动化":
    st.title("🤖 网页自动化配置")
    
    st.markdown("""
    ### 📋 说明
    
    网页自动化方案通过模拟浏览器操作实现视频发布，适合个人用户。
    
    **优点：**
    - 无需企业资质
    - 立即可用
    - 零成本
    
    **缺点：**
    - 可能触发风控
    - 需要维护登录状态
    - 稳定性不如官方 API
    
    **使用步骤：**
    1. 配置浏览器参数
    2. 运行登录脚本
    3. 扫码登录抖音
    4. 开始发布视频
    """)
    
    st.markdown("---")
    
    # 加载配置
    config = load_config()
    web_config = config.get("web_automation", {})
    
    # 配置表单
    col1, col2 = st.columns(2)
    
    with col1:
        browser = st.selectbox(
            "浏览器",
            ["chrome", "firefox"],
            index=0 if web_config.get("browser", "chrome") == "chrome" else 1
        )
        
        debug_port = st.number_input(
            "调试端口",
            value=web_config.get("debug_port", 9222),
            min_value=1000,
            max_value=65535
        )
    
    with col2:
        headless = st.checkbox(
            "无头模式",
            value=web_config.get("headless", False),
            help="无头模式不显示浏览器界面"
        )
        
        enabled = st.checkbox(
            "启用网页自动化",
            value=web_config.get("enabled", True)
        )
    
    # 登录状态
    st.markdown("---")
    st.subheader("🔐 登录状态")
    
    cookies_path = Path(config.get("storage", {}).get("cookies_path", "./storage/cookies"))
    cookie_file = cookies_path / f"{web_config.get('cookie_profile', 'default')}.json"
    
    if cookie_file.exists():
        st.success("✅ Cookie 文件存在，已登录")
        
        # 显示 Cookie 信息
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
            st.info(f"共 {len(cookies)} 个 Cookie")
    else:
        st.error("❌ 未登录，请先运行登录脚本")
        
        if st.button("🔑 运行登录脚本"):
            st.code("python scripts/quick_login.py", language="bash")
            st.info("运行后会打开浏览器，使用抖音 APP 扫码登录")
    
    # 保存按钮
    st.markdown("---")
    if st.button("💾 保存配置", use_container_width=True):
        config["web_automation"] = {
            "enabled": enabled,
            "browser": browser,
            "debug_port": debug_port,
            "headless": headless,
            "cookie_profile": "default"
        }
        save_config(config)
        st.success("✅ 配置已保存！")

# ==================== 发布视频 ====================
elif page == "📹 发布视频":
    st.title("📹 发布视频")
    
    # 加载配置
    config = load_config()
    
    # 选择发布方式
    publish_method = st.radio(
        "选择发布方式",
        ["官方 API", "网页自动化"],
        horizontal=True
    )
    
    st.markdown("---")
    
    # 视频文件选择
    st.subheader("1️⃣ 选择视频")
    
    videos_path = Path(config.get("storage", {}).get("videos_path", "./storage/videos"))
    if videos_path.exists():
        video_files = list(videos_path.glob("*.mp4"))
        if video_files:
            video_options = {str(f.name): str(f) for f in video_files}
            selected_video = st.selectbox(
                "选择视频文件",
                list(video_options.keys())
            )
            video_path = video_options[selected_video]
            
            # 显示视频信息
            video_size = os.path.getsize(video_path) / 1024 / 1024
            st.info(f"📹 {selected_video} ({video_size:.2f} MB)")
        else:
            st.warning("⚠️ 视频目录为空，请先添加视频文件")
            video_path = None
    else:
        st.error(f"❌ 视频目录不存在：{videos_path}")
        video_path = None
    
    # 视频信息
    st.subheader("2️⃣ 填写信息")
    
    col1, col2 = st.columns(2)
    
    with col1:
        title = st.text_input(
            "视频标题",
            placeholder="请输入视频标题",
            max_chars=50
        )
    
    with col2:
        hashtags = st.multiselect(
            "话题标签",
            ["#AI", "#自动化", "#科技前沿", "#短视频", "#干货"],
            default=["#AI", "#自动化"]
        )
    
    description = st.text_area(
        "视频描述",
        placeholder="请输入视频描述（可选）",
        height=100
    )
    
    # 组合文案
    full_text = f"{title} {' '.join(hashtags)}"
    if description:
        full_text += f"\n{description}"
    
    st.markdown("### 📝 预览文案")
    st.info(full_text)
    
    # 发布按钮
    st.markdown("---")
    
    if st.button("🚀 开始发布", type="primary", use_container_width=True):
        if not video_path:
            st.error("请先选择视频文件")
        elif not title:
            st.error("请填写视频标题")
        else:
            if publish_method == "官方 API":
                # 使用官方 API 发布
                if config.get("douyin_openapi", {}).get("enabled"):
                    client = DouyinOpenAPI(
                        config["douyin_openapi"]["client_key"],
                        config["douyin_openapi"]["client_secret"]
                    )
                    
                    # 加载 token
                    client.access_token = config["douyin_openapi"].get("access_token")
                    client.refresh_token = config["douyin_openapi"].get("refresh_token")
                    client.token_expires_at = config["douyin_openapi"].get("token_expires_at", 0)
                    
                    with st.spinner("正在发布视频..."):
                        # 上传
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        status_text.text("📹 正在上传视频...")
                        upload_result = client.upload_video(video_path, title)
                        progress_bar.progress(50)
                        
                        if upload_result.get("error_code") == 0:
                            video_id = upload_result.get("data", {}).get("video_id")
                            status_text.text("📝 正在发布视频...")
                            
                            # 发布
                            publish_result = client.create_video(video_id, full_text)
                            progress_bar.progress(100)
                            
                            if publish_result.get("error_code") == 0:
                                st.success("✅ 发布成功！")
                                st.json(publish_result)
                            else:
                                st.error(f"❌ 发布失败：{publish_result.get('description', '未知错误')}")
                        else:
                            st.error(f"❌ 上传失败：{upload_result.get('description', '未知错误')}")
                else:
                    st.error("请先在【官方 API 配置】页面配置并启用官方 API")
            
            else:
                # 使用网页自动化发布
                if config.get("web_automation", {}).get("enabled"):
                    st.info("🤖 网页自动化发布功能开发中...")
                    st.code(
                        f"python scripts/publish.py --video {video_path} --title '{title}' --desc '{full_text}'",
                        language="bash"
                    )
                else:
                    st.error("网页自动化未启用")

# ==================== 视频管理 ====================
elif page == "📊 视频管理":
    st.title("📊 视频管理")
    
    st.info("💡 此功能需要官方 API 支持")
    
    # 加载配置
    config = load_config()
    
    if config.get("douyin_openapi", {}).get("enabled"):
        # 初始化客户端
        client = DouyinOpenAPI(
            config["douyin_openapi"]["client_key"],
            config["douyin_openapi"]["client_secret"]
        )
        client.access_token = config["douyin_openapi"].get("access_token")
        client.refresh_token = config["douyin_openapi"].get("refresh_token")
        client.token_expires_at = config["douyin_openapi"].get("token_expires_at", 0)
        
        if st.button("🔄 刷新视频列表"):
            with st.spinner("正在获取视频列表..."):
                result = client.list_videos(count=20)
                
                if result.get("error_code") == 0:
                    videos = result.get("data", {}).get("list", [])
                    
                    if videos:
                        for video in videos:
                            with st.expander(f"📹 {video.get('title', '无标题')}"):
                                st.write(f"**视频 ID:** {video.get('video_id')}")
                                st.write(f"**描述:** {video.get('text')}")
                                st.write(f"**创建时间:** {datetime.fromtimestamp(video.get('create_time', 0))}")
                                st.write(f"**状态:** {'公开' if video.get('is_top') == 0 else '私密'}")
                                
                                # 操作按钮
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    if st.button("📊 查看数据", key=f"data_{video.get('video_id')}"):
                                        data_result = client.get_video_data(video.get('video_id'))
                                        if data_result.get("error_code") == 0:
                                            st.json(data_result.get("data", {}))
                                
                                with col2:
                                    if st.button("🗑️ 删除视频", key=f"delete_{video.get('video_id')}"):
                                        delete_result = client.delete_video(video.get('video_id'))
                                        if delete_result.get("error_code") == 0:
                                            st.success("✅ 删除成功")
                                            st.rerun()
                                        else:
                                            st.error(f"❌ 删除失败：{delete_result.get('description', '未知错误')}")
                    else:
                        st.info("暂无视频")
                else:
                    st.error(f"❌ 获取失败：{result.get('description', '未知错误')}")
    else:
        st.warning("请先配置并启用官方 API")
