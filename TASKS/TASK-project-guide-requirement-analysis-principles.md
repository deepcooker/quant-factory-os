# TASK: project-guide requirement-analysis principles

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-project-guide-requirement-analysis-principles
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
提炼需求分析指南中适合 AI/Codex 的原则，并最小增强 PROJECT_GUIDE/WORKFLOW/ENTITIES。

## Scope
- `docs/`
- `tools/`

## Non-goals

## Acceptance
- [x] PROJECT_GUIDE 增强学习追问；WORKFLOW/ENTITIES 同步新主线下的需求收敛边界；不引回旧流程

## Inputs
- `tools/需求管理及分析工作指南.doc`
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`

## Task Summary
- Status: completed

### Key Updates
- 从需求分析指南中提炼出适合 AI/Codex 的需求收敛原则，并补到 `PROJECT_GUIDE` 的 Q9-Q12 标准答案中。
- `WORKFLOW` 已补 run 主线程在新主线下需要确认的背景、边界、影响面、风险、非功能和验收规则。
- `ENTITIES` 已补 run/task 的需求边界字段建议，以及 `run-main/dev/test/arch` 的角色定义。

### Decisions
- 不恢复旧 `orient/choose/council/arbiter` 为正式流程，只迁移其有价值的需求收敛方法到新主线。
- 优先增强 `PROJECT_GUIDE` 的高质量提问能力，再让 `WORKFLOW` 和 `ENTITIES` 承接稳定结构字段。

### Risks
- 当前只是文档层增强，task/run 的结构化字段还未全面落到 JSON 真相源。

### Verification
- 已检查 `PROJECT_GUIDE` 的 Q9-Q12、`WORKFLOW` 的 run 方向收敛与多角色拆解段落、`ENTITIES` 的 run/task/thread 定义。

### Next Steps
- 继续从需求管理文档中提炼少量可迁移原则，优先服务 `PROJECT_GUIDE` 的学习协议增强。
- 后续再评估哪些边界字段需要正式进入 `TASKS/TASK-*.json` 与 `run_summary.json`。

### Source Threads
- `019ce5e2-50f1-7b20-aadf-4b746a1d1467`

## Risks / Rollback
- Risks: 
- Rollback plan:
