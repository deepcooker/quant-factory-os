# TASK: ship 成功后自动同步本地 main 到最新（无需手动 enter）

RUN_ID: run-2026-02-25-ship-main-enter
OWNER: <you>
PRIORITY: P1

## Goal
解决单人开发“PR 合并后本地 main 不更新”的摩擦：在 tools/ship.sh 成功结束时强制执行 git 同步，把本地 main fast-forward/rebase 到 origin/main 最新，避免每次手动 ./tools/enter.sh 才看到最新队列与代码。

## Scope (Required)
- `tools/`
- `tests/`
- `docs/`
- `TASKS/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- ship 成功后（PR 创建/合并流程结束），脚本会自动执行 sync：`git fetch` + `git checkout main` + `git pull --rebase origin main`，并打印同步后的 main HEAD。
- 同步前若工作区不干净，明确报错并退出（不做隐式覆盖）。
- 不引入额外慢检查：不调用 doctor/pytest（只做 git 同步）。
- 更新 docs/WORKFLOW.md：说明“ship 后 main 已自动同步，本地无需再手动 enter 才能看到最新”。
- `make verify` 全绿，并为该 RUN_ID 写齐 evidence 三件套。

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
