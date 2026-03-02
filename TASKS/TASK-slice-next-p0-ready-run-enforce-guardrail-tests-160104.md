# TASK: slice-next: P0: ready 先处理未收尾 run（收尾/抛弃） - enforce guardrail tests

RUN_ID: run-2026-03-02-slice-next-p0-ready-run-enforce-guardrail-tests
OWNER: <you>
PRIORITY: P1

## Goal
Add or refine guardrail tests to lock behavior of the selected direction.

## Scope (Required)
- `tests/`
- `tools/qf`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- [ ] critical path regression tests added or refreshed
- [ ] failure-path assertions are explicit and actionable
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
