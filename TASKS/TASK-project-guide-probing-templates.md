# TASK: project-guide probing templates

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-project-guide-probing-templates
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
从需求分析指南中提炼少量可迁移的高质量追问模板，最小增强 PROJECT_GUIDE，不改题库结构。

## Scope
- `docs/`

## Non-goals

## Acceptance
- [x] PROJECT_GUIDE 在不改题号和结构的前提下补少量高质量追问模板

## Inputs
- `tools/需求管理及分析工作指南.doc`
- `docs/PROJECT_GUIDE.md`

## Task Summary
- Status: completed

### Key Updates
- 在 `PROJECT_GUIDE` 的 Q9-Q12 下补了少量高质量追问模板，不改题库结构。
- 追问模板重点覆盖需求背景、范围边界、不做项、影响面、异常流、非功能和验收。

### Decisions
- 只增强 `PROJECT_GUIDE` 的学习与提问质量，不把传统需求管理文档整份迁入。
- 追问模板优先服务 run 方向收敛、角色协作边界和对象分层判断。

### Risks
- 当前模板仍是文档级提示，尚未变成结构化 prompt 生成器。

### Verification
- 已检查 `PROJECT_GUIDE` 的 Q9-Q12 段落并确认题号和结构未变化。

### Next Steps
- 继续从需求分析原则中筛出少量可复用模板，服务 AI 面对杂乱客户材料时的自我梳理。

### Source Threads
- `019ce5e2-50f1-7b20-aadf-4b746a1d1467`

## Risks / Rollback
- Risks: 
- Rollback plan:
