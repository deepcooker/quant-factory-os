# TASK: project-guide markdown draft template

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-project-guide-markdown-draft-template
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
将客户杂乱材料读完后的 AI 标准化 markdown 草稿模板沉淀到协议层，不改实现。

## Scope
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`

## Non-goals
- 不实现自动生成器
- 不改 appserverclient/taskclient/evidence 主流程

## Acceptance
- [x] PROJECT_GUIDE 增加最小 markdown 草稿模板; WORKFLOW/ENTITIES 只做必要口径同步; evidence updated

## Inputs
- `tools/需求管理及分析工作指南.doc`
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`

## Task Summary
- Status: completed

### Key Updates
- 在 `PROJECT_GUIDE` 的 Q12 下新增标准化 `Markdown intake draft` 模板，用于 AI 读完客户材料后的首轮结构化输出。

### Decisions
- `Markdown intake draft` 只作为 run 级协议层草稿，不作为机器真相源。

### Risks
- 如果后续把 intake draft 误当成 `run summary` 或 task 真相源，仍可能造成分层混乱。

### Verification
- `docs/PROJECT_GUIDE.md` 已新增模板
- `docs/WORKFLOW.md` 与 `docs/ENTITIES.md` 已同步其定位

### Next Steps
- 继续讨论是否需要把该模板抽成可复用的独立 markdown 提示模板。

### Source Threads
- `fork_current_session`

## Risks / Rollback
- Risks: 
- Rollback plan:
