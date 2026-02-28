# Summary

RUN_ID: `run-2026-03-01-qf-sync-ready`

## What changed
- Added `tools/qf sync [RUN_ID=...]`:
  - Auto-reads mandatory sync/governance/startup files.
  - Writes `reports/<RUN_ID>/sync_report.json` and `sync_report.md`.
  - Reports file-read list, project north-star summary, constitution/workflow/skills lookup entry, current run stage, session continuity, and one next command.
- Added sync gate enforcement to `tools/qf ready`:
  - Requires valid `sync_report.json`.
  - Default behavior auto-runs `tools/qf sync` when missing (`QF_READY_AUTO_SYNC=1`).
  - Writes sync gate status into `ready.json` under `sync_gate`.
- Hardened readiness validation:
  - `ready_file_is_valid` now checks sync gate by default (`QF_READY_REQUIRE_SYNC=1`).
- Improved `tools/qf plan` low-friction behavior:
  - Resolves plan run-id from current state by default.
  - Auto-stashes dirty workspace before sync/pick proposal.
  - Correctly cleans untracked `TASKS/TODO_PROPOSAL.md` to preserve clean-tree contract.
- Added automatic conversation checkpoint updates for key sync gating commands:
  - `tools/qf sync` and `tools/qf ready` append to `reports/<RUN_ID>/conversation.md`.
- Added/updated tests:
  - New: `tests/test_qf_sync_gate.py` (sync report generation + ready auto-sync + ready fail when auto-sync disabled).
  - Updated: `tests/test_qf_ready_gate.py`, `tests/test_qf_current_run.py`, `tests/test_qf_execution_log.py`, `tests/test_qf_plan_clean.py`.
- Updated owner docs for process change:
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - `SYNC/README.md`
  - `SYNC/READ_ORDER.md`

## Commands / Outputs
- `make verify`
  - `86 passed in 12.70s`
- `tools/qf sync RUN_ID=run-2026-03-01-qf-sync-ready`
  - `SYNC_PASS: true`
  - `SYNC_FILES_READ: 22`
  - `SYNC_MISSING_REQUIRED: 0`
  - `SYNC_REPORT_FILE: reports/run-2026-03-01-qf-sync-ready/sync_report.json`
- `tools/qf ready RUN_ID=run-2026-03-01-qf-sync-ready`
  - `SYNC_AUTO_RUN: tools/qf sync RUN_ID=run-2026-03-01-qf-sync-ready`
  - `READY_FILE: reports/run-2026-03-01-qf-sync-ready/ready.json`
  - `READY_SYNC_REPORT: reports/run-2026-03-01-qf-sync-ready/sync_report.json`

## Notes
- `tools/qf plan` keeps clean-tree guarantees; execution/conversation logging for plan was intentionally not added to avoid polluting working tree.
- For compatibility with old fixture-style tests that construct minimal repos, tests explicitly set `QF_READY_REQUIRE_SYNC=0` where sync files are intentionally absent.
