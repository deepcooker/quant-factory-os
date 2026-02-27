# TASK: p0-sync-state-machine-doc-gates

RUN_ID: run-2026-02-27-p0-sync-state-machine-doc-gates
OWNER: codex
PRIORITY: P0

## Goal
Codify a single source-of-truth session state machine and hard documentation
freshness gates so sync remains low-friction but auditable.

## Scope (Required)
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `SYNC/README.md`
- `SYNC/READ_ORDER.md`
- `SYNC/CURRENT_STATE.md`
- `SYNC/DECISIONS_LATEST.md`
- `SYNC/SESSION_LATEST.md`
- `TASKS/STATE.md`
- `TASKS/TASK-p0-sync-state-machine-doc-gates.md`
- `reports/run-2026-02-27-p0-sync-state-machine-doc-gates/`

## Non-goals
- No changes to `tools/qf` behavior in this run.
- No plan/do refactor in this run.
- No strategy/wealth content changes.

## Acceptance
- [x] Command(s) pass: `make verify`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [x] State machine + hard doc gate clearly documented in owner docs

## Inputs
- User requirement: sync must improve automation efficiency, not add friction.
- Hard rule: document updates are mandatory for process changes.

## Steps (Optional)
1. Add explicit lifecycle state machine and command boundaries.
2. Add hard documentation freshness gate and stop-reason taxonomy.
3. Align SYNC entry docs with init/handoff/ready semantics.
4. Verify and ship.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: rule duplication across AGENTS/WORKFLOW/SYNC.
- Rollback plan: revert this RUN diff.
