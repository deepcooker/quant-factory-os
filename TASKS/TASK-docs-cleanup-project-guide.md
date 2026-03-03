# TASK: docs cleanup: PROJECT_GUIDE 仅保留问答 + 新增财富系统新建项目引导

RUN_ID: run-2026-03-04-docs-cleanup-project-guide
OWNER: <you>
PRIORITY: P1

## Goal
把同频入口压缩成“问题-标准回答”格式，并单独提供财富系统项目落地引导文档，降低新会话学习噪音。

## Scope (Required)
- `docs/PROJECT_GUIDE.md`
- `docs/WEALTH_SYSTEM_NEW_PROJECT_GUIDE.md`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- [ ] `docs/PROJECT_GUIDE.md` 仅保留问答条目（问题+回答+证据），不保留其他叙述章节
- [ ] 新增财富系统新建项目引导文件并包含可执行步骤清单
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- Links / files / references
- If data is needed, specify allowed sample constraints (max rows, time window)

## Steps (Optional)
Suggested approach, if you have one.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks:
- Rollback plan:
