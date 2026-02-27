# TASK: p1-qf-low-friction-init-handoff-ready

RUN_ID: run-2026-02-27-p1-qf-low-friction-init-handoff-ready
OWNER: codex
PRIORITY: P1

## Goal
Reduce friction in session startup by improving `tools/qf init/handoff/ready`
without touching `plan/do` flow.

## Scope (Required)
- `tools/qf`
- `tests/test_qf_handoff.py`
- `tests/test_qf_ready_gate.py`
- `tests/test_qf_current_run.py`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `SYNC/README.md`
- `SYNC/CURRENT_STATE.md`
- `SYNC/DECISIONS_LATEST.md`
- `SYNC/SESSION_LATEST.md`
- `TASKS/STATE.md`
- `TASKS/TASK-p1-qf-low-friction-init-handoff-ready.md`
- `reports/run-2026-02-27-p1-qf-low-friction-init-handoff-ready/`

## Non-goals
- No changes to `tools/qf plan` and `tools/qf do`.
- No strategy/wealth content changes.
- No branch/PR policy changes.

## Acceptance
- [x] Command(s) pass: `make verify`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [x] `init/handoff/ready` friction reduced with backward compatibility

## Inputs
- User feedback: sync should reduce workload, not increase manual steps.
- P0 baseline: state machine and doc freshness gate already merged.

## Steps (Optional)
1. `init`: continuing run path should be clearer and lower-friction.
2. `ready`: support low-friction auto-fill from task/state defaults.
3. `handoff`: provide clearer next-command recommendation.
4. Update docs and tests.
5. Verify and ship.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: behavior drift with existing tests/scripts.
- Rollback plan: revert this RUN diff.
