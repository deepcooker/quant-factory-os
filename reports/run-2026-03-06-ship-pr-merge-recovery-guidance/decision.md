# Decision

RUN_ID: `run-2026-03-06-ship-pr-merge-recovery-guidance`

## Why
- PR #168 proved the current `pr_merge_blocked` stop was correct but under-specified.
- The next smallest improvement is to make the recovery path explicit and reproducible without changing merge authority.

## Options considered
- Add explicit recovery guidance and state fields only.
- Auto-run `git fetch origin <base> && git merge origin/<base>` inside `ship.sh`.
- Leave recovery entirely manual and undocumented.

## Risks / Rollback
- Automatic conflict repair remains intentionally out of scope for this slice.
- If the recovery wording later proves too narrow, rollback is simple: revert the `ship.sh` guidance lines and the matching tests/docs.
