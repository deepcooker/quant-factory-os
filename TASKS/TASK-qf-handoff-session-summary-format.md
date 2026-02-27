# TASK: qf-handoff-session-summary-format

RUN_ID: run-2026-02-27-qf-handoff-session-summary-format
OWNER: codex
PRIORITY: P1

## Goal
Make `tools/qf handoff` generate a concise "session summary" by default, focusing on communication highlights, key conclusions, and one next action.

## Scope (Required)
- `tools/qf`
- `tests/test_qf_handoff.py`
- `docs/WORKFLOW.md`
- `SYNC/SESSION_LATEST.md`
- `TASKS/STATE.md`
- `TASKS/TASK-qf-handoff-session-summary-format.md`
- `reports/run-2026-02-27-qf-handoff-session-summary-format/`

## Non-goals
- No changes to strategy/wealth content.
- No changes to `tools/qf do` and ship flow.
- No full chat transcript storage in repo.

## Acceptance
- [x] `tools/qf handoff` output defaults to concise summary structure.
- [x] Existing handoff behavior remains robust for missing inputs.
- [x] `make verify` passes.
- [x] Evidence updated under `reports/{RUN_ID}/`.

## Inputs
- User request: "`SESSION_LATEST` 保留总结，不要细节流水账；基于文件总结。"

## Steps (Optional)
1. Update handoff writer template in `tools/qf`.
2. Adjust tests to new summary contract.
3. Verify and update evidence.

## Risks / Rollback
- Risk: existing expectations/tests around old handoff sections may break.
- Rollback plan: revert this RUN diff.
