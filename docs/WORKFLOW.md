# WORKFLOW

Standard start

This document describes the expected workflow for changes in this repository.

## Status snapshot rule
Before each ship, record `/status` output in the evidence for the active RUN_ID.

## File list rule
`project_all_files.txt` is a local generated artifact and is excluded from PRs by
default. Update it only with a dedicated task, and call out the change in the PR
body.

## Scope gate rule
Task files must declare a `## Scope` section with allowed change paths. `tools/ship.sh`
validates staged files against this declared scope by default.

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
  `reports/{RUN_ID}/decision.md` (key decisions), and `MISTAKES/` (postmortems
  when enabled).
- When sharing code with an external model, use `project_all_files.txt` as the
  context snapshot. It is ignored by default and must only be updated via a
  dedicated task with explicit approval to commit.
- Hard rule (gate): Uncommitted changes do not exist for other agents or cloud runs.
- Hard rule (gate): Handoff must be via PR or commit hash, with evidence under
  `reports/{RUN_ID}/`.
- Hard rule (gate): If local-only context is needed, record it as structured evidence
  (`summary.md`, `decision.md`, `MISTAKES/`) or in `TASKS/STATE.md`, not in chat.

## Codex session startup checklist
- Do not rely on chat/session memory; rely only on repo memory:
  `TASKS/STATE.md`, `TASKS/QUEUE.md`, `reports/{RUN_ID}/`.
- Preferred entrypoint: `tools/qf` (`init/plan/do/resume`).
- Compatibility wrappers: `tools/enter.sh` and `tools/onboard.sh` forward to `tools/qf`.
- 1) Read `TASKS/STATE.md` via `tools/view.sh` and treat it as the only current progress baseline.
- 2) If STATE shows an active RUN_ID, read `reports/{RUN_ID}/summary.md` and
  `reports/{RUN_ID}/decision.md`.
- 3) 对外统一入口：先运行 `tools/qf init`（自动 stash 可恢复 + sync main + doctor + onboard）。
- 4) 运行 `tools/qf ready RUN_ID=<run-id>` 完成复述上岗门禁（会写入 `reports/<run-id>/ready.json`）。
- 5) 运行 `tools/qf plan 20` 生成候选；该命令会复制 proposal 到 `/tmp`（并打印路径）且保持工作区干净。
- 6) 运行 `tools/qf do queue-next` 领取下一枪（内部确保 ready + plan 前置、自动 evidence）。
- 7) Expand that item into `TASKS/TASK-*.md` (from template), then run:
  implement minimal diff -> `make verify` -> update reports -> `tools/task.sh` ship.
- Ship failure recovery: `tools/ship.sh` writes `reports/{RUN_ID}/ship_state.json`
  at key steps. On push/PR/merge/sync failure, run `tools/qf resume RUN_ID=...`.
- Ship success behavior: after merge, ship auto-syncs local `main` to `origin/main`.
- 7) On failure, write failure reason, repro, and next step in
  `reports/{RUN_ID}/summary.md` + `reports/{RUN_ID}/decision.md` (and `MISTAKES/`
  or `TASKS/STATE.md` when needed).

## Codex governance and automation
- Session constitution: `docs/CODEX_ONBOARDING_CONSTITUTION.md`
- Default policy: PR-driven flow with local `make verify`; do not depend on GitHub Actions queues.
- If automation is ever re-enabled, it must be explicitly requested and documented in task acceptance.
- `tools/ship.sh` hard gate blocks `.github/workflows/*.yml|*.yaml` by default; explicit override required:
  - `SHIP_ALLOW_WORKFLOWS=1 tools/ship.sh "<msg>"`
