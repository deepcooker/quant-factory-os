# Drift Review

RUN_ID: `run-2026-03-02-contract-next-p0-ready-run`
Generated At (UTC): 2026-03-02T06:38:34.010592+00:00
Status: `pass`
Strict: `false` | Auto-fix: `true` | Non-blocking: `true`

## Checks
- [pass] summary_file: reports/run-2026-03-02-contract-next-p0-ready-run/summary.md exists (raw)
- [pass] decision_file: reports/run-2026-03-02-contract-next-p0-ready-run/decision.md exists (raw)
- [warn] ready_gate: reports/run-2026-03-02-contract-next-p0-ready-run/ready.json missing (raw)
- [warn] direction_choice: reports/run-2026-03-02-contract-next-p0-ready-run/orient_choice.json missing (raw)
- [warn] direction_contract: reports/run-2026-03-02-contract-next-p0-ready-run/direction_contract.json missing (raw)
- [warn] verify_record: missing verify record -> auto-fixed placeholder (fixed)
- [warn] stop_reason: missing stop reason -> auto-fixed placeholder (fixed)
- [pass] task_contract: TASKS/TASK-contract-next-p0-ready-run.md exists (raw)

## Fixes
- added verify record placeholder in summary
- added stop reason placeholder in decision

## Blockers
- none

## Next Command
- `tools/qf do queue-next`
