# WORKFLOW

Standard start

This document describes the expected workflow for changes in this repository.

## Status snapshot rule
Before each ship, record `/status` output in the evidence for the active RUN_ID.

## File list rule
`project_all_files.txt` is a local generated artifact and is excluded from PRs by
default. Update it only with a dedicated task, and call out the change in the PR
body.

## Context snapshot (for ChatGPT)
`project_all_files.txt` is a context index snapshot for external models. It is
not evidence and does not belong in PRs by default. If it must be updated,
create a dedicated task, set `SHIP_ALLOW_FILELIST=1`, and use
`git add -f project_all_files.txt`.

## Memory & Context (handoff rules)
- Do not store full chat transcripts or raw logs in the repo. Keep them local
  under `chatlogs/` and ensure it is listed in `.gitignore`.
- Repo memory is limited to: `docs/` (rules), `TASKS/STATE.md` (current state),
  `reports/<RUN_ID>/decision.md` (key decisions), and `MISTAKES/` (postmortems
  when enabled).
- When sharing code with an external model, use `project_all_files.txt` as the
  context snapshot. It is ignored by default and must only be updated via a
  dedicated task with explicit approval to commit.
- Hard rule: Uncommitted changes do not exist for other agents or cloud runs.
- Hard rule: Handoff must be via PR or commit hash, with evidence under
  `reports/<RUN_ID>/`.
- Hard rule: If local-only context is needed, record it as structured evidence
  (`summary.md`, `decision.md`, `MISTAKES/`) or in `TASKS/STATE.md`, not in chat.
