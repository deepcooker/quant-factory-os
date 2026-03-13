# TASK: project-guide self-structuring skeleton

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-project-guide-self-structuring-skeleton
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
把高质量追问进一步压成客户材料输入后的 AI 自我梳理输出骨架，最小增强 PROJECT_GUIDE。

## Scope
- `docs/`

## Non-goals

## Acceptance
- [x] PROJECT_GUIDE 增加最小自我梳理输出骨架，不改题库结构

## Inputs
- `docs/PROJECT_GUIDE.md`
- `tools/需求管理及分析工作指南.doc`

## Task Summary
- Status: completed

### Key Updates
- 在 `PROJECT_GUIDE` 的 Q9-Q12 下补了客户材料输入后的 AI 自我梳理输出骨架。
- 输出骨架把 run 方向、角色计划、对象分层和 task 前置边界收成最小结构。

### Decisions
- 继续只增强协议层，不新增实现层工具或结构化生成器。
- 输出骨架直接挂在现有题目下，避免新增独立章节稀释课程主线。

### Risks
- 当前骨架仍是文档约定，尚未自动生成 JSON。

### Verification
- 已检查 `PROJECT_GUIDE` 的 Q9-Q12 段落，确认题库结构和题号保持不变。

### Next Steps
- 后续可以继续把这些骨架映射到 task/run 真相源字段，但当前先维持协议层。

### Source Threads
- `019ce5e2-50f1-7b20-aadf-4b746a1d1467`

## Risks / Rollback
- Risks: 
- Rollback plan:
