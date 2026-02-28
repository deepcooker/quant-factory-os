# TASK: qf resume 已合并场景避免重复创建 PR

RUN_ID: run-2026-02-28-qf-resume-pr
OWNER: codex
PRIORITY: P1

## Goal
当 `tools/qf resume` 读取到的 `ship_state` 对应 PR 已经 `MERGED` 时，直接走本地同步收尾，不再重复创建新 PR。

## Scope (Required)
- `tools/qf`
- `tests/`
- `docs/WORKFLOW.md`
- `TASKS/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- [x] 复现路径下（`ship_state` 已有 `pr_url` 且 PR 已合并），`tools/qf resume` 不再调用 `gh pr create`。
- [x] 仍完成 `checkout main + pull --rebase origin main`，并输出 `resume done`。
- [x] 新增/更新回归测试覆盖该分支逻辑。
- [x] `make verify` 通过，证据写入 `reports/{RUN_ID}/`。

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
