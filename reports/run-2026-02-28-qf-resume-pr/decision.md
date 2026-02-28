# Decision

RUN_ID: `run-2026-02-28-qf-resume-pr`

## Why
- Real incident: `tools/qf resume` re-created a PR after the original PR had already merged, because `ship_state.json` may persist early step (`branch_prepared`) with empty `pr_url`.
- This caused duplicate PR noise and extra merge churn.

## Options considered
- Keep current behavior and rely on manual cleanup (rejected): still creates duplicate PRs under stale ship_state.
- Only trust `ship_state.pr_url` (rejected): stale/empty `pr_url` is exactly the failure mode.
- Add merged-PR detection before any branch/push/create step (chosen): robust to stale `ship_state` and minimizes side effects.

## Risks / Rollback
- Risk: false positive merged lookup could skip needed resume steps.
- Mitigation: lookup is constrained by `--head <branch> --base main --state merged`, and we still run main sync.
- Rollback: revert this RUN to restore previous resume behavior.
