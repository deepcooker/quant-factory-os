# Decision

RUN_ID: `run-2026-02-27-housekeeping-clean-transient-reports`

## Why
- After ship+resume, recurring transient report files kept showing as untracked and added friction to daily flow.
- We needed a minimal fix that keeps workspace clean without hiding core evidence files.

## Options considered
- Manual cleanup only (rejected): solves once but repeats every session.
- Broad ignore for `reports/run-*/` (rejected): too aggressive and can hide real evidence.
- Minimal targeted ignore + immediate cleanup (chosen): lowest risk and repeatable.

## Risks / Rollback
- Risk: `mistake_log.jsonl` becomes ignored by default; intentional commit requires explicit force add.
- Rollback: remove the two ignore entries from `.gitignore` and restore prior behavior.
