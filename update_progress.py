#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
进度监控数据生成器
读取 task_plan.md 并生成 progress_data.json 供 HTML 使用
"""
import re
import json
from datetime import datetime
from pathlib import Path
import sys
import io

# 设置 UTF-8 输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def parse_task_plan(md_file):
    """解析 task_plan.md 文件"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    phases = []
    current_phase = None
    current_module = None
    
    lines = content.split('\n')
    
    for line in lines:
        # 检测阶段标题
        phase_match = re.match(r'^## 📝 Phase (\d+): (.+)$', line)
        if phase_match:
            if current_phase:
                phases.append(current_phase)
            
            current_phase = {
                'number': int(phase_match.group(1)),
                'name': f"Phase {phase_match.group(1)}: {phase_match.group(2)}",
                'status': 'pending',
                'progress': 0,
                'tasks': []
            }
            continue
        
        # 检测模块标题
        module_match = re.match(r'^#### (\d+\.\d+) (.+)$', line)
        if module_match and current_phase:
            current_module = {
                'id': module_match.group(1),
                'name': module_match.group(2)
            }
            continue
        
        # 检测任务
        task_match = re.match(r'^- \[([ x])\] (.+)$', line)
        if task_match and current_phase:
            status = 'done' if task_match.group(1) == 'x' else 'pending'
            current_phase['tasks'].append({
                'name': task_match.group(2),
                'status': status
            })
    
    if current_phase:
        phases.append(current_phase)
    
    # 计算每个阶段的进度
    for phase in phases:
        total = len(phase['tasks'])
        done = sum(1 for t in phase['tasks'] if t['status'] == 'done')
        phase['progress'] = (done / total * 100) if total > 0 else 0
        
        # 更新阶段状态
        if done == total:
            phase['status'] = 'done'
        elif done > 0:
            phase['status'] = 'in_progress'
        else:
            phase['status'] = 'pending'
    
    return phases

def generate_json(phases, output_file):
    """生成 JSON 数据文件"""
    data = {
        'title': '六位一体 - 智能内容生产流水线',
        'phases': phases,
        'last_update': datetime.now().isoformat()
    }
    
    # 计算总体统计
    total = sum(len(p['tasks']) for p in phases)
    completed = sum(sum(1 for t in p['tasks'] if t['status'] == 'done') for p in phases)
    in_progress = sum(1 for p in phases if p['status'] == 'in_progress')
    
    data['stats'] = {
        'total_tasks': total,
        'completed_tasks': completed,
        'in_progress_tasks': in_progress,
        'overall_progress': (completed / total * 100) if total > 0 else 0
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    return data['stats']

def update_html_progress(html_file, stats):
    """更新 HTML 中的进度数据（简单版本）"""
    # 这个函数可以扩展为动态更新 HTML
    pass

if __name__ == '__main__':
    workspace = Path('C:/Users/爽爽/.openclaw/workspace')
    
    print("=" * 60)
    print("进度监控数据生成器")
    print("=" * 60)
    print()
    
    # 解析 task_plan.md
    task_plan = workspace / 'task_plan.md'
    if not task_plan.exists():
        print(f"❌ 文件不存在：{task_plan}")
        exit(1)
    
    print(f"[OK] Reading: {task_plan}")
    phases = parse_task_plan(task_plan)
    
    # 生成 JSON
    json_file = workspace / 'progress_data.json'
    print(f"[OK] Generated: {json_file}")
    stats = generate_json(phases, json_file)
    
    # 显示统计
    print()
    print("=" * 60)
    print("Project Statistics")
    print("=" * 60)
    print(f"Total tasks: {stats['total_tasks']}")
    print(f"Completed: {stats['completed_tasks']}")
    print(f"In progress: {stats['in_progress_tasks']}")
    print(f"Progress: {stats['overall_progress']:.1f}%")
    print()
    print(f"[OK] Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print(f"URL: file:///{workspace / 'progress.html'}")
