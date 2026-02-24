# TASK: Session 一键初始化（onboard）+ 串行接下一枪（after-ship next）

RUN_ID: run-2026-02-24-session-onboard-after-ship-next
OWNER: <you>
PRIORITY: P1

## Goal
新增一次-session 的自动入职/对齐脚本（同步+环境确认+必读清单+强制复述模板+最近 decision/PR 摘要），并在 ship 成功后自动提示下一枪命令（可选自动生成下一 TASK_FILE+RUN_ID，但不自动改代码）。

## Scope (Required)
- `tools/`
- `tests/`
- `docs/`
- `TASKS/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- 新增入口：`tools/onboard.sh`（或 `make onboard`）可运行；输出包含：宪法/背景/阶段/工作流/复述模板/最近 decision 入口。
- ship 成功后输出 “下一枪建议”：若 QUEUE 还有 `[ ]`，提示 `tools/task.sh --next`；可选：在开关启用时自动执行 `--next` 并打印 TASK_FILE/RUN_ID。
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
