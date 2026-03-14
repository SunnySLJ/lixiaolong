# Planning with Files - 安装完成

## ✅ 安装状态

**安装位置：**
```
C:\Users\爽爽\.openclaw\workspace\skills\planning-with-files\
├── SKILL.md              # 技能说明
├── templates/            # 模板文件
├── scripts/              # 辅助脚本
└── references/           # 参考资料
```

**版本：** v2.22.0

---

## 🚀 快速开始

### 方式 1：自动初始化（推荐）

在项目中运行：

```powershell
powershell -ExecutionPolicy Bypass -File C:\Users\爽爽\.openclaw\workspace\skills\planning-with-files\scripts\init.ps1
```

### 方式 2：手动创建

在项目根目录创建三个文件：

1. **task_plan.md** - 任务计划和阶段跟踪
2. **findings.md** - 调研发现和笔记
3. **progress.md** - 进展日志和测试结果

---

## 📋 核心工作流

```
1. 接收复杂任务
     ↓
2. 创建 task_plan.md（分解任务）
     ↓
3. 执行任务，记录 findings.md
     ↓
4. 更新 progress.md（日志）
     ↓
5. 完成每个阶段后更新 task_plan.md
     ↓
6. 任务完成！
```

---

## 📁 文件说明

### task_plan.md
**用途：** 任务分解、阶段跟踪、决策记录

**结构：**
```markdown
# Task Plan

## Goal
[任务目标]

## Phases
- [ ] Phase 1: [名称]
- [ ] Phase 2: [名称]
- [ ] Phase 3: [名称]

## Decisions
[关键决策记录]

## Errors
[遇到的错误和解决方案]
```

### findings.md
**用途：** 调研笔记、发现、参考资料

**结构：**
```markdown
# Findings

## [主题 1]
- 发现 1
- 发现 2

## [主题 2]
- ...
```

### progress.md
**用途：** 会话日志、测试结果、进展追踪

**结构：**
```markdown
# Progress Log

## Session 1 (2026-03-13)
- 完成：XXX
- 问题：XXX
- 下一步：XXX
```

---

## 💡 最佳实践

### ✅ 应该做的

1. **先规划，后执行** - 永远先创建 task_plan.md
2. **每 2 次搜索后保存** - 重要发现立即写入 findings.md
3. **决策前读计划** - 保持目标在注意力窗口
4. **阶段后更新** - 完成后立即标记状态
5. **记录所有错误** - 避免重复踩坑

### ❌ 不应该做的

1. 不要跳过规划直接执行
2. 不要只在脑子里记住信息
3. 不要等到最后才更新进度
4. 不要隐藏错误

---

## 🎯 使用场景

**适合：**
- ✅ 多步骤项目（>5 个工具调用）
- ✅ 复杂调研任务
- ✅ 需要追踪进展的长期任务
- ✅ 团队协作项目

**不适合：**
- ❌ 简单问答
- ❌ 单步骤任务
- ❌ 即时查询

---

## 🔧 辅助脚本

| 脚本 | 用途 |
|------|------|
| `init.ps1` | 初始化规划文件 |
| `check-complete.sh` | 检查阶段完成度 |

---

## 📖 更多资源

- **官方文档：** https://github.com/OthmanAdi/planning-with-files
- **模板目录：** `skills/planning-with-files/templates/`
- **示例目录：** `skills/planning-with-files/examples/`

---

## 🦞 下一步

规划系统已就绪！现在可以：

1. **创建 ScriptBot** - 根据热点生成视频脚本
2. **创建 VideoBot** - 自动视频制作
3. **开始规划项目** - 用 planning-with-files 管理你的"六位一体"流水线

**继续哪个？**

---

**安装时间：** 2026-03-13 15:57
**安装位置：** `C:\Users\爽爽\.openclaw\workspace\skills\planning-with-files\`
