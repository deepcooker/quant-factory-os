# Summary

RUN_ID: `run-2026-02-27-sync-learning-exam-cli-web`

## What changed
- Added cross-surface sync exam assets under `SYNC/`:
  - `SYNC/EXAM_PLAN_PROMPT.md` (`/plan` prompt pack for CLI + web GPT)
  - `SYNC/EXAM_ANSWER_TEMPLATE.md` (fixed answer structure)
  - `SYNC/EXAM_RUBRIC.json` (weighted required checks)
  - `SYNC/EXAM_WORKFLOW.md` (execution and grading flow)
- Added deterministic grader script: `tools/sync_exam.py`
  - Reads markdown answer sections
  - Grades with rubric
  - Emits pass/fail + score + failed checks
  - Writes auditable json output
- Added regression tests: `tests/test_sync_exam.py`
- Updated sync/governance docs to include exam flow:
  - `SYNC/README.md`
  - `SYNC/READ_ORDER.md`
  - `SYNC/LINKS.md`
  - `docs/WORKFLOW.md`
- Added scored sample output for this run:
  - `reports/run-2026-02-27-sync-learning-exam-cli-web/onboard_answer.md`
  - `reports/run-2026-02-27-sync-learning-exam-cli-web/sync_exam_result.json`

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-sync-learning-exam-cli-web`
- `/root/policy/venv/bin/python tools/sync_exam.py --answer-file reports/run-2026-02-27-sync-learning-exam-cli-web/onboard_answer.md --rubric-file SYNC/EXAM_RUBRIC.json --output-file reports/run-2026-02-27-sync-learning-exam-cli-web/sync_exam_result.json --run-id run-2026-02-27-sync-learning-exam-cli-web`
  - `SYNC_EXAM_PASS: true`
  - `SYNC_EXAM_SCORE: 100.0`
- `make verify`
  - `75 passed`

## Notes
- This run focuses on thought-layer alignment quality gates; execution gates remain unchanged.
