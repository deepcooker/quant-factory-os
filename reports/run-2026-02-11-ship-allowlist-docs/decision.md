# Decision

RUN_ID: `run-2026-02-11-ship-allowlist-docs`

## Why
- New untracked docs files should be shipped with task changes; previously they could be omitted because `docs/*` was missing from allowlist.
- Fixing allowlist plus a focused regression test prevents silent omissions in future shipping runs.

## Options considered
- Edit allowlist in `stage_changes()` only (chosen): smallest behavior change that directly addresses the gap.
- Add broader staging logic for all untracked files: rejected due to higher risk and scope expansion.
- End-to-end ship integration test: rejected for this task due to external `gh/remote` dependency and non-minimal scope.

## Risks / Rollback
- Risk: string-based test is tied to current allowlist formatting.
- Rollback plan: revert this run's changes in `tools/ship.sh`, `tests/test_ship_untracked_allowlist.py`, and run evidence files.
