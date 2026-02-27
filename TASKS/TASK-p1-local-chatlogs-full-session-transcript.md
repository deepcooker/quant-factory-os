# TASK: p1-local-chatlogs-full-session-transcript

RUN_ID: run-2026-02-27-p1-local-chatlogs-full-session-transcript
OWNER: codex
PRIORITY: P1

## Goal
Persist full Codex terminal session transcripts to local `chatlogs/` (gitignored)
so session continuity has a complete fallback without storing transcripts in repo.

## Scope (Required)
- `tools/start.sh`
- `tests/test_startup_entrypoints_contract.py`
- `docs/WORKFLOW.md`
- `SYNC/README.md`
- `SYNC/SESSION_LATEST.md`
- `TASKS/STATE.md`
- `TASKS/TASK-p1-local-chatlogs-full-session-transcript.md`
- `reports/run-2026-02-27-p1-local-chatlogs-full-session-transcript/`

## Non-goals
- No transcript storage inside tracked repository files.
- No changes to `tools/qf plan/do`.
- No strategy/wealth content changes.

## Acceptance
- [x] Command(s) pass: `make verify`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [x] `tools/start.sh` supports local full-session transcript logging under `chatlogs/`

## Inputs
- User choice: use local `chatlogs/` for complete session transcript fallback.

## Steps (Optional)
1. Add transcript logging behavior to `tools/start.sh`.
2. Keep opt-out switch for compatibility.
3. Update docs and tests.
4. Verify and ship.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: platform differences if terminal `script` utility is missing.
- Rollback plan: revert this RUN diff.
