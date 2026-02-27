# Decision

RUN_ID: `run-2026-02-27-governance-convergence-sync-priority`

## Why
- Existing governance docs had repeated and partially conflicting operational
  rules across `README.md`, `AGENTS.md`, `docs/WORKFLOW.md`, and `chatlogs`.
- Session continuity required one stable run pointer independent of chat memory.
- User explicitly approved:
  - canonical `PROJECT_GUIDE` under `docs/`
  - `CURRENT_RUN_ID` source-of-truth in `TASKS/STATE.md`.

## Options considered
- Option A: docs-only cleanup, no tooling behavior changes.
  - Rejected: would not remove run-id ambiguity in real execution.
- Option B: tooling-only changes without owner-map convergence.
  - Rejected: likely to reintroduce conflicts in future docs updates.
- Option C: converge docs ownership + implement `CURRENT_RUN_ID` defaults in `qf`.
  - Selected: smallest complete path to sync-first continuity.

## Risks / Rollback
- Risks:
  - Behavior change for users relying on explicit `RUN_ID` per command.
  - Potential mismatch friction when `CURRENT_RUN_ID` is stale.
- Mitigation:
  - Explicit run-id still supported.
  - Mismatch message is fail-fast with one-shot override flag:
    `QF_ALLOW_RUN_ID_MISMATCH=1`.
- Rollback:
  - Revert this RUN diff (docs + `tools/qf` + tests).
