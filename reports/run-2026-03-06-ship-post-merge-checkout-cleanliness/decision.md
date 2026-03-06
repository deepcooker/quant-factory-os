# Decision

RUN_ID: `run-2026-03-06-ship-post-merge-checkout-cleanliness`

## Why
- A real `ship` run merged PR `#169` successfully but then failed local post-ship sync because `tools/ship.sh` rewrote the tracked `ship_state.json` on the success path.
- That behavior dirtied the worktree after merge and blocked checkout back to the base branch, breaking local continuity even though the remote delivery had already succeeded.

## Options considered
- Keep writing `ship_state.json` on `merged` and `synced`, and add more stash/restore logic around checkout.
- Stop writing tracked `ship_state.json` on the success path, while preserving failure/recovery writes.
- Move runtime success state to a separate sidecar file.

## Risks / Rollback
- This change reduces post-merge success-state detail in `ship_state.json`; the authoritative success signal remains the merged PR plus run evidence.
- Rollback is straightforward: restore the removed `write_ship_state "merged"` / `write_ship_state "synced"` calls if a later design chooses a different persistence strategy.

## Stop Reason
- task_done
