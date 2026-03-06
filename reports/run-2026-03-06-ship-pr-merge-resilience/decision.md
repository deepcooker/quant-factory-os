# Decision

RUN_ID: `run-2026-03-06-ship-pr-merge-resilience`

## Why
- The second real smoke proved post-ship sync no longer self-blocked on `ship_state.json`, but then exposed a new gap: `ship.sh` still tried a direct merge on a PR that GitHub had already reported as non-cleanly mergeable.

## Options considered
- Keep retrying `gh pr merge` and rely on GitHub output alone.
- Detect non-clean merge state first and stop in a recoverable state before the direct merge step.

Chosen:
- Detect non-clean merge state first and fail with `pr_merge_blocked`.

## Risks / Rollback
- Risk: `mergeStateStatus` can be `UNKNOWN`, so the script still has to allow the old merge path in that case.
- Rollback: revert to the prior direct-merge behavior if the extra `gh pr view --json mergeStateStatus` call proves unstable in practice.

## Stop Reason
- task_done
