# Summary

RUN_ID: `run-2026-03-02-qf-v1-l1-do-plan`

## What changed
- Added L1 direction-layer commands in `tools/qf`:
  - `tools/qf orient [RUN_ID=...]` generates ranked direction options from `docs/PROJECT_GUIDE.md`, governance docs, state and run evidence.
  - `tools/qf choose [RUN_ID=...] OPTION=<id>` confirms one direction and writes `orient_choice.json`.
- Upgraded `tools/qf do queue-next` for low-friction stability:
  - Moved `do_start` execution logging to after `sync_main` to avoid dirty-worktree conflicts before `git pull`.
  - Fixed auto-plan/pick chain: missing proposal now triggers `bash tools/task.sh --plan 20` directly and proceeds to pick.
  - Added explicit queue-empty guidance: when pick fails with no `[ ]` queue item, prints next action `tools/qf orient RUN_ID=<run-id>`.
  - Auto-generated proposal files are cleaned up after pick success/failure to avoid temporary residue.
- Updated sync next-step hinting:
  - `tools/qf sync` now suggests `ready -> orient -> plan` progression based on run artifacts.
- Added regression tests for strong-mode behavior:
  - New `tests/test_qf_orient_and_do.py` covers orient/choose, do auto-plan chain, queue-empty hint, and do/sync ordering conflict regression.
- Updated owner docs to keep process truth aligned:
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - `SYNC/README.md`
  - `SYNC/READ_ORDER.md`

## Commands / Outputs
- `make verify`
  - `90 passed in 14.97s`
- `tools/qf ready RUN_ID=run-2026-03-02-qf-v1-l1-do-plan`
  - auto-ran sync and wrote `sync_report.json`, `ready.json`
- `tools/qf orient RUN_ID=run-2026-03-02-qf-v1-l1-do-plan`
  - `ORIENT_OPTIONS: 3`
  - `ORIENT_RECOMMENDED: stability-do-plan`
- `tools/qf choose RUN_ID=run-2026-03-02-qf-v1-l1-do-plan`
  - `CHOOSE_OPTION: stability-do-plan`
  - wrote `reports/run-2026-03-02-qf-v1-l1-do-plan/orient_choice.json`

## Notes
- This run implements L1 direction gating plus P0 execution friction fixes, while keeping execution still serial (parallel execution remains future work).
- `tools/qf do` still keeps recoverability (`print_resume_cmd`) on failure paths.
