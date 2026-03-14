# -*- coding: utf-8 -*-
"""
智小红 - 小红书数据自动化采集
使用 Playwright 浏览器自动化，带时间间隔控制
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path
import pandas as pd
from playwright.async_api import async_playwright

class XHSDataCollector:
    """小红书数据采集器"""
    
    def __init__(self, output_dir='xhs_data'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.collected_data = []
        
        # 频率控制（安全值）
        self.delay_per_note = 6  # 每条笔记间隔 6 秒
        self.delay_per_batch = 60  # 每批间隔 60 秒
        self.max_per_batch = 10  # 每批最多 10 条
        self.max_per_hour = 50  # 每小时最多 50 条
    
    async def collect_hot_topics(self, keywords, limit=20):
        """
        采集热点笔记
        
        Args:
            keywords: 搜索关键词列表
            limit: 总数量限制
        """
        print("=" * 60)
        print(f"开始采集小红书热点数据")
        print(f"关键词：{keywords}")
        print(f"目标数量：{limit}条")
        print("=" * 60)
        print()
        
        async with async_playwright() as p:
            # 启动浏览器
            browser = await p.chromium.launch(
                headless=False,  # 显示浏览器窗口
                slow_mo=100  # 降低操作速度，更像真人
            )
            
            # 创建上下文（模拟真实用户）
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            page = await context.new_page()
            
            try:
                # 登录小红书（需要用户手动登录一次）
                print("[1/3] Please login to Xiaohongshu...")
                await page.goto('https://www.xiaohongshu.com')
                await page.wait_for_timeout(5000)  # 等待用户登录
                
                # 等待用户确认登录成功
                input("[OK] Press Enter after login successful...")
                
                # 搜索并采集
                for i, keyword in enumerate(keywords, 1):
                    print(f"\n[2/3] 搜索关键词 ({i}/{len(keywords)}): {keyword}")
                    notes = await self.search_and_collect(page, keyword, limit // len(keywords))
                    self.collected_data.extend(notes)
                    
                    # 批次间隔
                    if i < len(keywords):
                        print(f"⏳ 等待 {self.delay_per_batch}秒...")
                        await asyncio.sleep(self.delay_per_batch)
                
                # 保存数据
                print(f"\n[3/3] 保存数据...")
                self.save_data()
                
                print(f"\n✅ 采集完成！共 {len(self.collected_data)} 条笔记")
                print(f"📁 数据已保存到：{self.output_dir}")
                
            finally:
                await browser.close()
        
        return self.collected_data
    
    async def search_and_collect(self, page, keyword, limit):
        """搜索并采集笔记"""
        notes = []
        
        # 进入搜索页面
        search_url = f'https://www.xiaohongshu.com/search_result?keyword={keyword}&source=web_search_result_notes'
        await page.goto(search_url)
        await page.wait_for_timeout(3000)  # 等待加载
        
        # 滚动页面加载更多内容
        print(f"  正在加载笔记列表...")
        for _ in range(3):
            await page.evaluate('window.scrollBy(0, 1000)')
            await asyncio.sleep(2)
        
        # 提取笔记列表
        note_elements = await page.query_selector_all('.note-item')
        
        print(f"  找到 {len(note_elements)} 条笔记，开始采集前 {min(limit, len(note_elements))} 条...")
        
        for i, note_el in enumerate(note_elements[:limit], 1):
            try:
                # 提取数据
                note_data = await self.extract_note_data(page, note_el)
                if note_data:
                    notes.append(note_data)
                    print(f"  ✓ [{i}/{limit}] {note_data['title'][:30]}... (点赞:{note_data['likes']})")
                
                # 间隔控制（关键！）
                if i < limit:
                    await asyncio.sleep(self.delay_per_note)
                
            except Exception as e:
                print(f"  ✗ 采集失败：{e}")
                continue
        
        return notes
    
    async def extract_note_data(self, page, note_el):
        """提取单条笔记数据"""
        try:
            # 标题
            title_el = await note_el.query_selector('.title')
            title = await title_el.inner_text() if title_el else ''
            
            # 点赞数
            likes_el = await note_el.query_selector('.like-count')
            likes = int(await likes_el.inner_text()) if likes_el else 0
            
            # 收藏数
            collect_el = await note_el.query_selector('.collect-count')
            collects = int(await collect_el.inner_text()) if collect_el else 0
            
            # 评论数
            comment_el = await note_el.query_selector('.comment-count')
            comments = int(await comment_el.inner_text()) if comment_el else 0
            
            # 作者
            author_el = await note_el.query_selector('.author-name')
            author = await author_el.inner_text() if author_el else ''
            
            # 链接
            link_el = await note_el.query_selector('a')
            link = await link_el.get_attribute('href') if link_el else ''
            
            return {
                'title': title,
                'author': author,
                'likes': likes,
                'collects': collects,
                'comments': comments,
                'link': f'https://www.xiaohongshu.com{link}' if link else '',
                'collected_at': datetime.now().isoformat(),
                'source': 'xiaohongshu'
            }
        except Exception as e:
            print(f"    提取失败：{e}")
            return None
    
    def save_data(self):
        """保存数据为多种格式"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # JSON 格式
        json_file = self.output_dir / f'xhs_data_{timestamp}.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.collected_data, f, ensure_ascii=False, indent=2)
        
        # Excel 格式
        if self.collected_data:
            df = pd.DataFrame(self.collected_data)
            excel_file = self.output_dir / f'xhs_data_{timestamp}.xlsx'
            df.to_excel(excel_file, index=False, engine='openpyxl')
            
            # CSV 格式
            csv_file = self.output_dir / f'xhs_data_{timestamp}.csv'
            df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        
        # 统计报告
        self.generate_report()
    
    def generate_report(self):
        """生成统计报告"""
        if not self.collected_data:
            return
        
        df = pd.DataFrame(self.collected_data)
        
        report = []
        report.append("=" * 60)
        report.append("小红书数据采集报告")
        report.append("=" * 60)
        report.append(f"采集时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"总笔记数：{len(df)}")
        report.append("")
        report.append("数据统计:")
        report.append(f"  平均点赞：{df['likes'].mean():.1f}")
        report.append(f"  平均收藏：{df['collects'].mean():.1f}")
        report.append(f"  平均评论：{df['comments'].mean():.1f}")
        report.append("")
        report.append("TOP 5 热门笔记:")
        top5 = df.nlargest(5, 'likes')[['title', 'likes', 'collects']]
        for i, row in top5.iterrows():
            report.append(f"  {i+1}. {row['title'][:40]}... (点赞:{row['likes']})")
        report.append("=" * 60)
        
        report_text = '\n'.join(report)
        print(report_text)
        
        # 保存报告
        report_file = self.output_dir / f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)

async def main():
    """主函数"""
    collector = XHSDataCollector(output_dir='xhs_data')
    
    # 定义要搜索的关键词（根据你的业务调整）
    keywords = [
        'AI 教程',
        '自媒体运营',
        '内容创作',
        '视频剪辑',
        '爆款技巧'
    ]
    
    # 开始采集
    await collector.collect_hot_topics(keywords, limit=50)

if __name__ == '__main__':
    asyncio.run(main())
