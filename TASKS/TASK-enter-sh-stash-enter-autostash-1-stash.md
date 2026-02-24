# TASK: enter.sh 支持显式自动 stash（ENTER_AUTOSTASH=1）并打印 stash 名

RUN_ID: run-2026-02-25-enter-sh-stash-enter-autostash-1-stash
OWNER: <you>
PRIORITY: P1

## Goal
解决单人开发常见摩擦：工作区不干净时 enter.sh 直接失败。新增显式开关 ENTER_AUTOSTASH=1，使 enter.sh 在同步前自动 git stash push -u，并打印 stash 名与恢复指令；默认行为保持严格失败。

## Scope (Required)
- `tools/enter.sh`
- `tests/`
- `docs/WORKFLOW.md`
- `TASKS/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- 默认 enter.sh：工作区不干净仍失败（不改变安全默认）。
- 设置 ENTER_AUTOSTASH=1 时：
- 自动 stash（含 untracked），并打印：stash 名 + 如何恢复（git stash list / pop）
- enter 正常继续 pull/doctor
- make verify 全绿
- docs/WORKFLOW.md 补充这一用法

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
