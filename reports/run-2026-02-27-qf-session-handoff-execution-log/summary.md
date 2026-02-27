# Summary

RUN_ID: `run-2026-02-27-qf-session-handoff-execution-log`

## What changed
- `tools/qf` enhancements:
  - Added structured execution logging to `reports/<RUN_ID>/execution.jsonl` with default redaction (`QF_LOG_REDACT=1`) and optional disable switch (`QF_LOG_DISABLE=1`).
  - Added `tools/qf handoff RUN_ID=<run-id>` to generate `reports/<RUN_ID>/handoff.md` from `ready.json`, `conversation.md`, `execution.jsonl`, and `ship_state.json`.
  - Added automatic events in `ready/do/resume/init` flows (`ready_passed`, `do_start`, `do_pick_success/fail`, resume failure/success events, init completed).
  - Added init reconnect hint: prints `tools/qf handoff RUN_ID=<latest>` when prior run evidence exists.
- Documentation updates:
  - `docs/WORKFLOW.md` now documents auto execution logs and handoff usage.
  - `AGENTS.md` now requires execution trace persistence and handoff-before-continue on reconnect.
- Added regression tests:
  - `tests/test_qf_execution_log.py`
  - `tests/test_qf_handoff.py`
- Added conversation checkpoint for this run:
  - `reports/run-2026-02-27-qf-session-handoff-execution-log/conversation.md`

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-qf-session-handoff-execution-log`
- `tools/qf snapshot RUN_ID=run-2026-02-27-qf-session-handoff-execution-log NOTE='Implemented P0-P2: auto execution logging with redaction, qf handoff generation, init handoff hint, and regression tests; make verify passed.'`
- `make verify` -> `64 passed in 4.93s`

## Notes
- Design keeps existing `init/ready/do/resume/snapshot` workflow intact and only adds one new subcommand (`handoff`).
