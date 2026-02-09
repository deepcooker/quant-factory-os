# Summary

RUN_ID: `run-2026-02-09-single-run-guard`

## What changed
- Added a single-run/task guard in `tools/ship.sh` and a pytest guardrail.

## Commands / Outputs
- Verify: `make verify`（已通过）

## Notes
- Why: 防串单（单任务单 RUN_ID）
- What: ship.sh 加护栏 + 最小测试
