def main() -> int:
    """主函数"""
    args = build_parser().parse_args()
    
    video_path = Path(args.video)
    cover_path = Path(args.cover) if args.cover else None
    
    # 检查文件
    ensure_file(video_path, "视频文件")
    if cover_path:
        ensure_file(cover_path, "封面文件")
    
    log("=" * 60)
    log("抖音视频上传")
    log("=" * 60)
    log(f"视频：{video_path.name}")
    log(f"标题：{args.title}")
    log(f"描述：{args.desc}")
    log(f"标签：{', '.join(args.tags)}")
    log(f"封面：{cover_path.name if cover_path else 'AI 智能封面'}")
    log("=" * 60)
    
    playwright = None
    browser = None
    page = None
    
    try:
        # 连接 Chrome
        playwright, browser, page = connect_to_chrome(args.debug_port)
        
        # 打开上传页面
        goto_upload_page(page)
        
        # 上传视频
        upload_video(page, video_path)
        
        # 等待 AI 封面生成
        wait_for_ai_cover(page)
        
        # 选择封面
        select_cover(page)
        
        # 填写信息
        fill_info(page, args.title, args.desc, args.tags)
        
        # 保存截图
        save_screenshot(page, "before_publish")
        
        # 点击发布
        if args.publish:
            click_publish(page)
            wait_for_publish(page)
            save_screenshot(page, "after_publish")
            log("=" * 60)
            log("发布完成！视频正在审核中")
            log("可以在抖音 APP 中查看审核状态")
            log("=" * 60)
        else:
            log("=" * 60)
            log("表单已准备好，未自动发布")
            log("请手动点击发布按钮")
            log("=" * 60)
        
        # 保持浏览器打开
        log("浏览器保持打开状态...")
        
        return 0
        
    except FileNotFoundError as e:
        log(f"文件错误：{e}")
        return 1
    except PlaywrightTimeoutError as e:
        log(f"操作超时：{e}")
        if page:
            save_screenshot(page, "error")
        return 1
    except Exception as e:
        log(f"上传失败：{e}")
        if page:
            save_screenshot(page, "error")
        return 1
    finally:
        # 关闭浏览器连接
        if playwright:
            try:
                playwright.stop()
            except:
                pass