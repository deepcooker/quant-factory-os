# TASK: 增加只读 Observer 周报（awareness digest）

RUN_ID: run-2026-02-24-observer-awareness-digest
OWNER: <you>
PRIORITY: P1

## Goal
新增只读观察器，从 repo 证据链（reports/*、TASKS/STATE.md、可选 MISTAKES/）生成周报报告，落到 reports/<RUN_ID>/awareness.md，形成可审计“学习产物”。

## Scope (Required)
- `Makefile`
- `tools/`
- `tests/`
- `docs/`
- `TASKS/`
- `reports/<RUN_ID>/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- 新增入口：`make awareness RUN_ID=<RUN_ID>`（或等价 tools/observe.sh）可运行。
- 输出：`reports/<RUN_ID>/awareness.md`，并在 summary/decision 里引用。
- 周报至少包含：本周 shipped runs（扫描 reports/run-*/decision.md）、重复失败模式（可选扫描 MISTAKES/）、当前风险（读 STATE）、下一枪建议（<=5 条、task-shaped）。
- `make verify` 全绿。

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
