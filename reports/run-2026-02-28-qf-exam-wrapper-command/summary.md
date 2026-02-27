# Summary

RUN_ID: `run-2026-02-28-qf-exam-wrapper-command`

## What changed
- Added `tools/qf exam` subcommand as one-command wrapper around `tools/sync_exam.py`.
- Wrapper behavior:
  - default run id: `TASKS/STATE.md` `CURRENT_RUN_ID`
  - default answer path: `reports/{RUN_ID}/onboard_answer.md`
  - default output path: `reports/{RUN_ID}/sync_exam_result.json`
  - default rubric path: `SYNC/EXAM_RUBRIC.json`
  - supports explicit args:
    - `RUN_ID=...`
    - `ANSWER_FILE=...`
    - `RUBRIC_FILE=...`
    - `OUTPUT_FILE=...`
- Added exam execution event logging via `execution.jsonl`.
- Added tests in `tests/test_qf_exam.py`:
  - default flow pass
  - custom path pass
  - missing answer fail
- Updated workflow docs to include one-command usage.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-28-qf-exam-wrapper-command`
- `make verify` -> `78 passed`

## Notes
- Goal is friction reduction: onboarding exam can now be graded with a single `tools/qf exam`.
