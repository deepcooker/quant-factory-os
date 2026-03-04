# Summary

RUN_ID: `run-2026-03-04-resume-self-block-fix`

## What changed
- Added a reliability fix in `tools/qf resume` to prevent self-blocking checkout:
  - before `resume_sync_checkout_main`, `cmd_resume` now calls
    `auto_stash_if_dirty "resume-cleanup-run-${run_id}"`.
  - this handles dirty workspace created by resume/ship trace updates
    (for example `execution.jsonl` / `ship_state.json`) and avoids checkout failure.
- Extended stash cleanup candidate matcher in `tools/qf`:
  - include `qf-resume-cleanup-run-*` pattern so auto-generated cleanup stashes can be cleaned by `tools/qf stash-clean`.
- Added regression coverage:
  - `tests/test_qf_current_run.py`
    - new test `test_qf_resume_autostash_before_checkout_main_when_dirty`
      verifies resume succeeds, auto-stash triggers, and current branch ends on `main`.
    - updated existing merged-PR lookup test to keep `gh.log` outside repo workspace.
  - `tests/test_qf_stash_clean.py`
    - include `qf-resume-cleanup-run-*` in cleanup candidate test matrix.
- Updated owner docs:
  - `AGENTS.md` documents resume auto-stash behavior before checkout main.
  - `docs/WORKFLOW.md` documents the same behavior in memory/context rules.
- Task lifecycle files for this run:
  - `TASKS/TASK-resume-self-block-fix.md`
  - `TASKS/QUEUE.md` (picked new item)
  - `TASKS/STATE.md` (active pointer to this run)

## Commands / Outputs
- `make evidence RUN_ID=run-2026-03-04-resume-self-block-fix`
  - wrote `meta.json`, ensured `summary.md` and `decision.md`
- `tools/qf sync RUN_ID=run-2026-03-04-resume-self-block-fix`
  - `SYNC_PASS: true`
- `tools/qf learn RUN_ID=run-2026-03-04-resume-self-block-fix MODEL_SYNC=1 PLAN_MODE=strong -log`
  - `LEARN_MODEL_SYNC_STATUS: pass`
  - oral/exam anchors emitted (`LEARN_MODEL_ORAL_*`, `LEARN_MODEL_ORAL_EXAM_QA_COUNT`)
- `tools/qf ready RUN_ID=run-2026-03-04-resume-self-block-fix`
  - passed with `READY_STEP[1/12] ... READY_STEP[12/12]`
- `tools/qf choose RUN_ID=run-2026-03-04-resume-self-block-fix OPTION=ready-exit-resolution`
  - generated `orient_choice.json` + `direction_contract.json|md`
- `make verify`
  - first run: 1 failure (existing resume lookup test needed adaptation for new auto-stash behavior)
  - final run: `124 passed in 52.41s`

## Notes
- `write.py` local modifications are user-owned and intentionally excluded from this run’s scope.
