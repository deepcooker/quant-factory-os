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
- The following hard rules are handoff gates and apply to every delivery.
- Do not store full chat transcripts or raw logs in the repo. Keep them local
  under `chatlogs/` and ensure it is listed in `.gitignore`.
- Repo memory is limited to: `docs/` (rules), `TASKS/STATE.md` (current state),
  `reports/<RUN_ID>/decision.md` (key decisions), and `MISTAKES/` (postmortems
  when enabled).
- When sharing code with an external model, use `project_all_files.txt` as the
  context snapshot. It is ignored by default and must only be updated via a
  dedicated task with explicit approval to commit.
- Hard rule (gate): Uncommitted changes do not exist for other agents or cloud runs.
- Hard rule (gate): Handoff must be via PR or commit hash, with evidence under
  `reports/<RUN_ID>/`.
- Hard rule (gate): If local-only context is needed, record it as structured evidence
  (`summary.md`, `decision.md`, `MISTAKES/`) or in `TASKS/STATE.md`, not in chat.

## Codex session startup checklist
- Do not rely on chat/session memory; rely only on repo memory:
  `TASKS/STATE.md`, `TASKS/QUEUE.md`, `reports/<RUN_ID>/`.
- 1) Read `TASKS/STATE.md` via `tools/view.sh` and treat it as the only current progress baseline.
- 2) If STATE shows an active RUN_ID, read `reports/<RUN_ID>/summary.md` and
  `reports/<RUN_ID>/decision.md`.
- 3) Read `TASKS/QUEUE.md` and pick the top unfinished queue item.
- 4) Expand that item into `TASKS/TASK-*.md` (from template), then run:
  `make evidence` -> implement minimal diff -> `make verify` -> update reports ->
  `tools/task.sh` ship.
- 5) On failure, write failure reason, repro, and next step in
  `reports/<RUN_ID>/summary.md` + `reports/<RUN_ID>/decision.md` (and `MISTAKES/`
  or `TASKS/STATE.md` when needed).
