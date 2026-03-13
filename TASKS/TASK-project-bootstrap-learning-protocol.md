# TASK: project bootstrap learning protocol

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-project-bootstrap-learning-protocol
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
为未接入基座的新项目定义最小同频学习与文档补齐协议，强调通用 PROJECT_GUIDE 先行。

## Scope
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`

## Non-goals
- 不实现跨项目复制工具
- 不修改 appserverclient/taskclient 运行时

## Acceptance
- [x] 新增最小 bootstrap 协议文档或章节; PROJECT_GUIDE/WORKFLOW/FILE_INDEX 口径同步; evidence updated

## Inputs
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `docs/ENTITIES.md`

## Task Summary
- Status: completed

### Key Updates
- 新增 `docs/PROJECT_BOOTSTRAP_PROTOCOL.md`，定义陌生项目尚未接入基座时的最小学习与文档补齐协议。
- 在 `PROJECT_GUIDE` 与 `WORKFLOW` 中补了最小入口，明确先 bootstrap 再进入正式主线。

### Decisions
- 通用 `PROJECT_GUIDE` 继续作为跨项目学习协议，项目化 owner docs 通过 bootstrap 协议逐步补齐。

### Risks
- 若后续把 bootstrap 协议误当成自动化接入脚本，会再次混淆学习层与实现层。

### Verification
- `docs/PROJECT_BOOTSTRAP_PROTOCOL.md` 已创建
- `docs/PROJECT_GUIDE.md`、`docs/WORKFLOW.md`、`docs/FILE_INDEX.md` 已同步引用

### Next Steps
- 继续讨论是否需要把陌生项目首轮 intake 输出再压成独立模板文件。

### Source Threads
- `fork_current_session`

## Risks / Rollback
- Risks: 
- Rollback plan:
