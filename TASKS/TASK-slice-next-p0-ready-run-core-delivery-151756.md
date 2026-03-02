# TASK: slice-next: P0: ready 先处理未收尾 run（收尾/抛弃） - core delivery

RUN_ID: run-2026-03-02-slice-next-p0-ready-run-core-delivery
OWNER: <you>
PRIORITY: P1

## Goal
避免把历史中断状态混入新需求，先做生命周期分流。

## Scope (Required)
- `tools/qf`
- `tests/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- [ ] deliver selected direction option `ready-exit-resolution` with bounded scope
- [ ] command(s) pass: make verify
- [ ] reports summary/decision updated for this slice
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
