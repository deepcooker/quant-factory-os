# Summary

RUN_ID: `run-2026-02-09-status-snapshot`

## What changed
- Documented a hard rule to record `/status` snapshots in evidence.
- Added a minimal guardrail test to keep the rule from regressing.

## Commands / Outputs
- `make verify`

## Notes
- `/status` snapshot (paste before starting work):
  ```markdown
  /status
  Model: <paste here>
  Account: <paste here>
  5h limit: <paste here>
  Weekly limit: <paste here>
  ```
