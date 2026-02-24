# Summary

RUN_ID: `run-2026-02-24-session-onboard-after-ship-next`

## What changed
- Added `tools/onboard.sh` as a one-shot session onboarding entrypoint that:
  - prints required entry links (`AGENTS.md`, `PROJECT_GUIDE.md`,
    `docs/WORKFLOW.md`, `TASKS/STATE.md`, `TASKS/QUEUE.md`)
  - prints forced-restatement template entry
  - lists recent `reports/run-*/decision.md` paths
  - writes auditable output to `reports/{RUN_ID}/onboard.md`
- Added ship success hint block in `tools/ship.sh`:
  - `== 下一枪建议 ==`
  - `如果 QUEUE 还有 [ ]：运行 tools/task.sh --next`
- Added tests:
  - `tests/test_onboard_smoke.py`
  - `tests/test_ship_next_hint.py`

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-24-session-onboard-after-ship-next`
- `bash tools/onboard.sh run-2026-02-24-session-onboard-after-ship-next`
  - `ONBOARD_FILE: ./reports/run-2026-02-24-session-onboard-after-ship-next/onboard.md`
- `make verify` -> `42 passed in 1.57s`

## Notes
- Did not auto-run `tools/task.sh --next` from ship; only emitted fixed next-shot hint.
