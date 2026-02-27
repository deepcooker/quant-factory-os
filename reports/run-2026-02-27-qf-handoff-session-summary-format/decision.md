# Decision

RUN_ID: `run-2026-02-27-qf-handoff-session-summary-format`

## Why
- User requested handoff/session memory to be concise summary instead of detailed sections.
- Goal is lower recovery friction after `/quit`, account switching, or unstable network.

## Options considered
- Keep existing detailed handoff layout (rejected): too verbose for quick continuity.
- Create separate new command for summary (rejected): increases command surface and user burden.
- Change `tools/qf handoff` default output to concise summary (chosen): same command, better UX.

## Risks / Rollback
- Risk: old tests or downstream expectations tied to prior section headers can break.
- Mitigation: updated handoff contract tests and ran full `make verify`.
- Rollback: revert this RUN diff (`tools/qf`, `tests/test_qf_handoff.py`, `docs/WORKFLOW.md`, `SYNC/SESSION_LATEST.md`, `TASKS/STATE.md`).
