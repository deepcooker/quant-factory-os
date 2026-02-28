# TASK: qf exam-auto 默认自动填答并自动评分

RUN_ID: run-2026-02-28-qf-exam-auto
OWNER: codex
PRIORITY: P1

## Goal
让 `tools/qf exam-auto` 在答卷缺失时默认自动生成可评分答案并立刻评分，避免人工先填模板再重跑。

## Scope (Required)
- `tools/qf`
- `tests/`
- `docs/WORKFLOW.md`
- `TASKS/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- [x] `tools/qf exam-auto` 在缺答卷时默认不再返回 3，而是自动填答并产出 `sync_exam_result.json`。
- [x] 保留手动模式开关（可显式只生成模板不自动填答）。
- [x] 新增/更新回归测试覆盖“默认自动化”和“手动模式”两条路径。
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
