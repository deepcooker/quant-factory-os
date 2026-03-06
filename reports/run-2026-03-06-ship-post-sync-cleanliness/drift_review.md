# Drift Review

RUN_ID: `run-2026-03-06-ship-post-sync-cleanliness`
Generated At (UTC): 2026-03-06T12:18:38.657760+00:00
Status: `pass`
Strict: `true` | Auto-fix: `true` | Non-blocking: `false`

## Checks
- [pass] summary_file: reports/run-2026-03-06-ship-post-sync-cleanliness/summary.md exists (raw)
- [pass] decision_file: reports/run-2026-03-06-ship-post-sync-cleanliness/decision.md exists (raw)
- [warn] ready_gate: reports/run-2026-03-06-ship-post-sync-cleanliness/ready.json missing (raw)
- [pass] direction_choice: reports/run-2026-03-06-ship-post-sync-cleanliness/orient_choice.json exists (raw)
- [pass] direction_contract: reports/run-2026-03-06-ship-post-sync-cleanliness/direction_contract.json exists (raw)
- [pass] verify_record: summary includes make verify record (raw)
- [pass] stop_reason: decision contains stop reason (raw)
- [pass] task_contract: TASKS/TASK-ship-post-sync-cleanliness.md exists (raw)

## Fixes
- none

## Blockers
- none

## Next Command
- `bash tools/legacy.sh do queue-next`
