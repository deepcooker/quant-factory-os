# Summary

RUN_ID: `run-2026-02-28-qf-resume-pr`

## What changed
- Updated `tools/qf` `cmd_resume` with merged-PR precheck:
  - if `ship_state.json` has `pr_url` and PR state is `MERGED`, skip `checkout/push/pr create/pr merge`
  - if `pr_url` is empty, lookup merged PR by head branch (`gh pr list --head <branch> --base main --state merged`)
  - when lookup finds merged PR, skip `checkout/push/pr create/pr merge`
  - continue with sync tail (`git checkout main` + `git pull --rebase origin main`)
- Added regression test `test_qf_resume_uses_merged_pr_lookup_without_create` in `tests/test_qf_current_run.py`.
- Updated `docs/WORKFLOW.md` Ship failure recovery note to document resume merged-PR short-circuit behavior.
- Updated task state pointers to this RUN in `TASKS/STATE.md`.

## Commands / Outputs
- `tools/task.sh --next`
  - `TASK_FILE: TASKS/TASK-qf-resume-pr.md`
  - `RUN_ID: run-2026-02-28-qf-resume-pr`
- `make verify`
  - `81 passed in 9.35s`

## Notes
- Fix target: avoid duplicate PR creation during `tools/qf resume` when the run has already been merged.
