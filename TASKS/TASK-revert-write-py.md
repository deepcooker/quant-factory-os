# TASK: revert unintended write.py change from merged PR #60

RUN_ID: run-2026-02-11-revert-write-py
OWNER: codex
PRIORITY: P1

## Goal
Revert the unintended `write.py` change from merged PR #60 only, without
modifying `docs/WORKFLOW.md`, `TASKS/STATE.md`, or handoff evidence in `reports/`.

## Non-goals
No changes to handoff rules or other project files.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-revert-write-py/summary.md` and `reports/run-2026-02-11-revert-write-py/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- `write.py` (current main version)
- PR #60 (merged)

## Steps (Optional)
1) Create evidence skeleton.
2) Revert `write.py` to the pre-PR #60 content.
3) Run `make verify`.
4) Update evidence and ship.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: Leaving unintended changes in `write.py`.
- Rollback plan: Revert the write.py change.
