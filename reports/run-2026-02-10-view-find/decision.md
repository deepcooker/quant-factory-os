# Decision

RUN_ID: `run-2026-02-10-view-find`

## Why
- Large file reading needed a low-friction pattern locator.

## What
- Extended `tools/view.sh` with `--find` and `--context` to report match line
  numbers and added tests for hit/miss behavior.

## Options considered
- Separate helper script (rejected: keep a single entry tool).

## Risks / Rollback
- Risk: Unexpected output format for callers relying on the tool.
- Rollback plan: Revert `tools/view.sh` and test file.

## Verify
- `make verify`
