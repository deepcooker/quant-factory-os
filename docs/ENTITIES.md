# ENTITIES

Entities

Minimal entity dictionary for existing repository objects and constraints.

## Task
- Definition: work contract for one change shot.
- Location: `TASKS/TASK-*.md` (template: `TASKS/_TEMPLATE.md`).
- Required fields: `RUN_ID`, `Goal`, `Acceptance`, `Scope`.
- Invariant: no code/doc change without an active task + RUN_ID (`AGENTS.md`).

## PR
- Definition: delivery unit for one task.
- Relation to Task: one task -> one branch -> one PR (`AGENTS.md`).
- Required title/body constraints: title must include RUN_ID; body must include
  `Why / What / Verify / Evidence paths`.
- Operational note: `tools/task.sh` passes task path/title into `tools/ship.sh`
  so PR body includes task/evidence sections.

## RUN_ID
- Definition: run namespace and identity for a task execution.
- Primary usage: evidence path prefix `reports/<RUN_ID>/`.
- Naming convention in repo: examples use `run-YYYY-MM-DD-...`.
- TODO/Assumptions: no single hard regex is defined in docs; keep current
  `run-<date>-<slug>` convention unless a stricter rule is added.

## CURRENT_RUN_ID
- Definition: the default active run pointer for session handoff and qf commands.
- Source-of-truth: `TASKS/STATE.md`.
- Related fields in `TASKS/STATE.md`:
  - `CURRENT_RUN_ID`
  - `CURRENT_TASK_FILE`
  - `CURRENT_STATUS` (`active|blocked|done`)
- Priority rule:
  - explicit command/env run id can override once;
  - otherwise tools resolve to `CURRENT_RUN_ID`;
  - fallback to latest evidence is allowed only as last resort with warning.

## Evidence
- Definition: structured memory under `reports/<RUN_ID>/`.
- Required files:
  - `meta.json`: run metadata scaffold (`make evidence`).
  - `summary.md`: what changed + commands/outputs + notes.
  - `decision.md`: why/options/risks.
- Minimum requirement: every task must create/update all three (`AGENTS.md`).

## STATE
- Definition: current progress baseline and startup entrypoint.
- Location: `TASKS/STATE.md` (single authoritative current-state file).
- Must contain: current conventions, next steps, current blockers/risks, and
  startup entry links (`docs/WORKFLOW.md` startup checklist).
- Usage rule: new sessions read STATE first, then queue/evidence.

## MISTAKES
- Definition: postmortem artifact for failures.
- When to write: task stuck or verify fails (`AGENTS.md` failure protocol).
- Format source: `ISSUES/PLAYBOOK.md` required fields (`issue_id`, `run_id`,
  `symptom`, `root_cause_type`, `evidence`, `fix_plan`, `guardrail_test`,
  `status`).
- Repo policy: optional, file path `MISTAKES/<RUN_ID>.md`, enabled only on
  failure path.

## Gate
- Enter gate: `tools/enter.sh` requires repo root, clean workspace, successful
  `git pull --rebase`, and passing `tools/doctor.sh`.
- Ship gate: `tools/ship.sh` enforces single-run guard, scope gate, filelist
  guard (`project_all_files.txt`), and self-guard for `tools/ship.sh`.
- Scope gate: staged files must match task `## Scope` + limited built-in
  exceptions (`reports/<RUN_ID>/`, `TASKS/STATE.md`, `TASKS/QUEUE.md`,
  `docs/WORKFLOW.md`).
- Denylist gate: `tools/view.sh` blocks reads matching `.codex_read_denylist`
  unless `CODEX_READ_DENYLIST_ALLOW=1`.

## Tool
- Definition: operational scripts under `tools/` for workflow execution.
- Covered scripts:
  - `tools/start.sh`: bootstrap venv/proxy, run enter, then exec codex.
  - `tools/enter.sh`: session entry checks and startup pointers.
  - `tools/doctor.sh`: environment/readiness checks.
  - `tools/view.sh`: constrained, range-based repo file reader.
  - `tools/task.sh`: select task and call ship with task metadata.
  - `tools/ship.sh`: commit/push/PR automation with gates.
  - `tools/run_a9`: TODO/Assumptions (not found as regular file in this repo).

## Artifact
- `docs/`: stable rules and conventions.
- `TASKS/`: task specs (`TASK-*`), queue, and current state.
- `reports/`: per-RUN_ID evidence and decisions.

## TODO/Assumptions
- RUN_ID hard-format rule is not centrally specified beyond current conventions.
- `tools/run_a9` is requested in dictionary scope but not present as a readable
  repo file; add when tool exists or document alias path.
