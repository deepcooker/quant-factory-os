# TASK: wire task->PR body and add evidence links

RUN_ID: run-2026-02-09-task-prbody
OWNER: codex
PRIORITY: P1

## Goal
Fix unused PR body generation in tools/task.sh and ensure tools/ship.sh PR body
includes task info and evidence paths per AGENTS rules.

## Non-goals
Do not change tools/ship.sh output when no related environment variables exist.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-task-prbody/summary.md` and `reports/run-2026-02-09-task-prbody/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- tools/task.sh
- tools/ship.sh
- TASKS/_TEMPLATE.md
- AGENTS.md

## Steps (Optional)
- Run `make evidence RUN_ID=run-2026-02-09-task-prbody`
- Update tools/task.sh to stop generating unused PR body and pass task info to ship
- Update tools/ship.sh to include task info and evidence paths when available
- Run `make verify`
- Update evidence reports
- Ship with SHIP_ALLOW_SELF=1

## Risks / Rollback
- Risks: PR body formatting regressions or incorrect run id parsing
- Rollback plan: revert tools/task.sh and tools/ship.sh
