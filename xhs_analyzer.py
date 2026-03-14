# -*- coding: utf-8 -*-
"""
小红书数据分析 - 自动生成热点报告
"""
import pandas as pd
import json
from pathlib import Path
from datetime import datetime

class XHSAnalyzer:
    """小红书数据分析师"""
    
    def __init__(self, data_dir='xhs_data'):
        self.data_dir = Path(data_dir)
    
    def analyze_latest(self):
        """分析最新采集的数据"""
        # 找到最新的 JSON 文件
        json_files = list(self.data_dir.glob('xhs_data_*.json'))
        if not json_files:
            print("❌ 未找到采集数据")
            return
        
        latest_file = max(json_files, key=lambda p: p.stat().st_mtime)
        print(f"分析文件：{latest_file.name}")
        
        # 加载数据
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not data:
            print("❌ 数据为空")
            return
        
        df = pd.DataFrame(data)
        
        # 生成分析报告
        report = self.generate_analysis(df)
        
        # 保存报告
        self.save_report(report, df)
        
        return report, df
    
    def generate_analysis(self, df):
        """生成深度分析报告"""
        report = []
        report.append("\n" + "=" * 80)
        report.append("🔥 小红书热点数据分析报告")
        report.append("=" * 80)
        report.append(f"生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"数据总量：{len(df)} 条笔记")
        report.append("")
        
        # 1. 整体统计
        report.append("📊 一、整体统计")
        report.append("-" * 80)
        report.append(f"平均点赞数：{df['likes'].mean():.1f}")
        report.append(f"平均收藏数：{df['collects'].mean():.1f}")
        report.append(f"平均评论数：{df['comments'].mean():.1f}")
        report.append(f"互动率 (赞 + 藏 + 评): {(df['likes'] + df['collects'] + df['comments']).mean():.1f}")
        report.append("")
        
        # 2. 爆款笔记分析
        report.append("🔥 二、爆款笔记 TOP 10")
        report.append("-" * 80)
        top10 = df.nlargest(10, 'likes')
        for i, row in top10.iterrows():
            report.append(f"{i+1}. {row['title'][:50]}")
            report.append(f"   点赞:{row['likes']} | 收藏:{row['collects']} | 评论:{row['comments']}")
            report.append(f"   作者:{row['author']}")
            report.append(f"   链接:{row['link']}")
            report.append("")
        
        # 3. 高收藏笔记（潜在爆款）
        report.append("⭐ 三、高收藏笔记 TOP 10 (潜在爆款)")
        report.append("-" * 80)
        top_collects = df.nlargest(10, 'collects')
        for i, row in top_collects.iterrows():
            report.append(f"{i+1}. {row['title'][:50]}")
            report.append(f"   收藏:{row['collects']} | 点赞:{row['likes']} | 收藏/赞比:{row['collects']/max(row['likes'],1):.2f}")
            report.append("")
        
        # 4. 标题关键词分析
        report.append("🔍 四、标题关键词分析")
        report.append("-" * 80)
        
        # 提取标题中的关键词（简化版）
        all_titles = ' '.join(df['title'].astype(str))
        
        # 常见热词（可以根据实际数据调整）
        hot_words = ['教程', '技巧', '攻略', '干货', '推荐', '必备', '神器', '方法', '分享', '经验']
        
        word_count = {}
        for word in hot_words:
            count = all_titles.count(word)
            if count > 0:
                word_count[word] = count
        
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        
        for word, count in sorted_words[:10]:
            report.append(f"  {word}: {count}次")
        report.append("")
        
        # 5. 作者分析
        report.append("👤 五、活跃作者 TOP 10")
        report.append("-" * 80)
        author_stats = df.groupby('author').agg({
            'likes': 'sum',
            'collects': 'sum',
            'title': 'count'
        }).rename(columns={'title': '笔记数'})
        
        author_stats['平均互动'] = (author_stats['likes'] + author_stats['collects']) / author_stats['笔记数']
        top_authors = author_stats.nlargest(10, '平均互动')
        
        for author, row in top_authors.iterrows():
            report.append(f"  {author}: {int(row['笔记数'])}篇 | 平均互动:{row['平均互动']:.1f}")
        report.append("")
        
        # 6. 内容建议
        report.append("💡 六、内容创作建议")
        report.append("-" * 80)
        
        # 分析爆款特征
        high_performers = df[df['likes'] > df['likes'].median()]
        if len(high_performers) > 0:
            avg_title_len = high_performers['title'].apply(len).mean()
            report.append(f"1. 爆款标题平均长度：{avg_title_len:.0f}字符")
            report.append(f"   建议：标题控制在 {avg_title_len-5:.0f}-{avg_title_len+5:.0f} 字符")
        
        # 高互动时间段（如果有时问数据）
        report.append("2. 发布建议:")
        report.append("   - 早高峰：7:00-9:00")
        report.append("   - 午休：12:00-14:00")
        report.append("   - 晚高峰：19:00-22:00")
        
        report.append("3. 内容方向:")
        if sorted_words:
            top_keywords = [w[0] for w in sorted_words[:3]]
            report.append(f"   热门话题：{', '.join(top_keywords)}")
        
        report.append("")
        report.append("=" * 80)
        
        return '\n'.join(report)
    
    def save_report(self, report_text, df):
        """保存报告"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # 文本报告
        report_file = self.data_dir / f'analysis_report_{timestamp}.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        # JSON 摘要
        summary = {
            'total_notes': len(df),
            'avg_likes': float(df['likes'].mean()),
            'avg_collects': float(df['collects'].mean()),
            'avg_comments': float(df['comments'].mean()),
            'top_10_titles': df.nlargest(10, 'likes')[['title', 'likes']].to_dict('records'),
            'generated_at': datetime.now().isoformat()
        }
        
        summary_file = self.data_dir / f'analysis_summary_{timestamp}.json'
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ 报告已保存:")
        print(f"   详细报告：{report_file}")
        print(f"   数据摘要：{summary_file}")

if __name__ == '__main__':
    analyzer = XHSAnalyzer()
    report, df = analyzer.analyze_latest()
    print(report)
