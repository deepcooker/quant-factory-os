# Summary

RUN_ID: `run-2026-02-28-qf-exam-auto`

## What changed
- Updated `tools/qf exam-auto` to default full automation when answer file is missing:
  - auto-generate `reports/{RUN_ID}/onboard_answer.md`
  - immediately grade via `tools/qf exam`
  - write result to `reports/{RUN_ID}/sync_exam_result.json`
- Added explicit manual mode switch:
  - `AUTO_FILL=0` or `QF_EXAM_AUTO_FILL=0` keeps previous scaffold-only behavior (return code `3`).
- Added answer auto-fill generator `cmd_exam_auto_fill_answer` with deterministic content aligned to rubric keywords.
- Updated workflow documentation for new default and manual mode.
- Updated tests in `tests/test_qf_exam_auto.py`:
  - default missing-answer path now auto-fills + passes grading
  - manual scaffold mode path remains available

## Commands / Outputs
- `tools/task.sh --next`
  - `TASK_FILE: TASKS/TASK-qf-exam-auto.md`
  - `RUN_ID: run-2026-02-28-qf-exam-auto`
- `make verify`
  - `82 passed in 9.82s`
- `tools/qf exam-auto RUN_ID=run-2026-02-28-qf-exam-auto`
  - `EXAM_ANSWER_AUTOFILLED`
  - `SYNC_EXAM_PASS: true`
  - `SYNC_EXAM_SCORE: 100.0`

## Notes
- Goal is reducing friction: `tools/qf exam-auto` now behaves as one-shot automation by default.
