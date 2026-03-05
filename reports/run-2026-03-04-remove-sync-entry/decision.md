# Decision

RUN_ID: `run-2026-03-04-remove-sync-entry`

## Why
- You requested a clean, shareable `AGENTS.md` that follows your logic: high automation, strong anti-drift, and explicit onboarding gate around `PROJECT_GUIDE`.
- You requested additional test minimization: remove `a9` test files, merge qf tests into a minimal module, and drop sync-related failing test blocks.

## Options considered
- Keep previous long AGENTS with many legacy details.
- Rebuild AGENTS into a lighter hard-contract file and move details to owner docs.
- Decision: rebuild into lighter hard-contract version with explicit owner map and startup gate.
- Keep existing split qf tests and patch failures incrementally.
- Collapse qf tests to one minimal smoke module and delete sync gate tests.
- Decision: collapse to minimal test surface (`tests/task_qf.py`) and remove target files per request.
- Keep remaining non-qf tests split by original filenames.
- Collapse all remaining test modules into `task_{module}.py` minimal smoke suite.
- Decision: collapse all remaining `tests/test_*.py` into module-level `tests/task_*.py` files.
- Keep old init behavior (`auto-stash + sync-main + doctor + auto-handoff`) and continue as implicit workflow step.
- Redefine init as pure environment diagnostic with mode flags and explicit status output.
- Decision: redefine init as diagnostic-only and split behavior by mode (`check`, `-status`, `-main`).
- Keep init details duplicated in AGENTS and WORKFLOW.
- Decision: AGENTS keeps gate contract only; init step details stay in WORKFLOW (`S0 Environment`) with explicit pointer in AGENTS.

## Risks / Rollback
- Risk: some wording may differ from older docs until full cross-doc pass is completed.
- Rollback: restore previous `AGENTS.md` from git history if this contract is rejected.
- Risk: significant coverage reduction in qf/sync paths; regressions may slip undetected.
- Rollback: restore deleted test files from git history and reintroduce focused cases incrementally.
- Risk: broader test minimization reduces behavioral guarantees across ship/task/start/view flows.
- Rollback: recover prior `tests/test_*.py` files from history by module and re-enable incrementally.
- Risk: users accustomed to side-effectful init may miss old auto actions.
- Rollback: restore prior `cmd_init` implementation from git history and re-enable auto-* actions if needed.

## Incremental decision (learn must be real model sync)
### Why
- Requirement is explicit: onboarding must be true same-frequency understanding, not local-script-only pseudo pass.
- Allowing `MODEL_SYNC=0/auto` and `PLAN_MODE=basic` leaves downgrade paths that can bypass true comprehension.

### Options considered
- Keep backward-compatible modes (`MODEL_SYNC=0|auto|1`, `PLAN_MODE=strong|basic`).
- Force hard mode (`MODEL_SYNC=1`, `PLAN_MODE=strong`) and fail fast when Codex/model sync is unavailable.
- Decision: force hard mode and remove downgrade path for learn gate.

### Implemented contract
- `tools/qf learn` rejects non-strict sync/plan args.
- Learn parser now requires model `files_read` to cover required onboarding file set.
- `learn_file_is_valid` now requires strong model sync result before `ready` accepts learn evidence.
- Docs updated in same run (`AGENTS.md`, `docs/WORKFLOW.md`, `docs/PROJECT_GUIDE.md`).

### Risk / rollback
- Risk: environments without working `codex` auth/network can no longer pass learn.
- Rollback: revert strict checks in `tools/qf` and docs to previous compatibility behavior.

## Incremental decision (learn core = plan + oral + practice + mainline anchor)
### Why
- Requirement changed from “通过 learn”到“真正同频”：必须同时体现
  - 高质量问答口述（读文档后回答）
  - 实操痕迹（沙盒命令实践）
  - 主线回拉（明确对应 PROJECT_GUIDE 问题点与偏移纠正动作）
- Existing strong mode lacked explicit “回拉锚点映射” and explicit “实践包”字段约束。

### Options considered
- Keep existing strong schema (plan/oral/exam only) and rely on人工解释回拉主线。
- Extend strong schema with explicit anchor+practice packets and enforce them in learn validity.
- Decision: extend schema and enforce at gate level.

### Implemented contract
- `tools/qf learn` strong parse now requires:
  - `anchor_realign` (`question_id` must be `Q1..Q17`, `status`, `drift_detail`, `return_to_mainline`)
  - `practice` (derived from model events, requires command_execution evidence)
- Console now prints the same anchor/practice fields to make session-visible alignment explicit.
- `learn_file_is_valid` now rejects learn artifacts missing these new packets.
- `docs/PROJECT_GUIDE.md`:
  - removed Q18
  - Q16 evidence moved away from historical `reports/run-*` samples to codex docs + `test_codex/artifacts/*`.
- `docs/WORKFLOW.md` updated with new learn anchor outputs.

### Risk / rollback
- Risk: model occasionally under-fills new fields, making learn stricter and more failure-prone.
- Rollback: relax parser requirements for `anchor_realign` / `practice` keys in `tools/qf` and `learn_file_is_valid`.

## Incremental decision (console readability only)
### Why
- Current learn output contains complete anchors but is hard to scan quickly in terminal.
- Requirement: keep strict gates unchanged while improving operator experience.

### Decision
- Add a concise readout section to stdout (`LEARN_READOUT_*`) after strong-mode anchors.
- Keep all existing machine anchors and validation logic unchanged.

### Risk / rollback
- Risk: slightly longer stdout.
- Rollback: remove `LEARN_READOUT_*` print block from `tools/qf` without affecting gates.

## Incremental decision (learn timeout/log defaults)
### Why
- Requirement: simplify operator UX so learn runs with full visibility by default.
- Manual `-log` and shorter default timeout increased unnecessary friction.

### Decision
- Set `learn` defaults to:
  - `MODEL_TIMEOUT_SEC=300` (unless overridden)
  - log mirror enabled by default (`QF_LEARN_LOG=1`)
- Keep strict same-frequency gates unchanged (`MODEL_SYNC=1`, `PLAN_MODE=strong`).

### Risk / rollback
- Risk: default run writes one extra log file each learn invocation.
- Rollback: revert `QF_LEARN_LOG` default to `0` and keep `-log` as manual opt-in.

## Incremental decision (make /plan wrapper honest + deterministic)
### Why
- You required learn to be true same-frequency onboarding, not pseudo `/plan`.
- In this environment PTY devices can be unavailable, so interactive slash transport may not run.
- We need deterministic, visible transport behavior instead of silent ambiguity.

### Decision
- Introduce explicit transport control in learn:
  - `PLAN_TRANSPORT=auto|slash|exec` (`auto` default)
  - `auto` resolves to `slash` only when PTY is available; otherwise resolves to `exec`.
- Keep strong plan protocol schema mandatory regardless of transport.
- Surface transport truth in stdout:
  - requested transport
  - auto reason
  - effective transport
- Bind oral exam to `PROJECT_GUIDE` Q-bank by enforcing `question_id=Q1..Q17` per item.

### Risk / rollback
- Risk: `slash` transport can fail on hosts without PTY support.
- Mitigation: `PLAN_TRANSPORT=auto` default keeps learn usable and still strict.
- Rollback: set `QF_LEARN_PLAN_TRANSPORT=exec` permanently and remove slash branch if operationally unnecessary.

## Incremental decision (make learn Python-first, keep Bash as wrapper)
### Why
- You requested Python as primary logic runtime and Bash as thin shell.
- Current learn behavior had already moved to mixed Bash+inline-Python and became hard to maintain.
- Python-first implementation gives deterministic parsing/validation and easier future migration of other commands.

### Decision
- Introduce `tools/qf_learn.py` as the canonical implementation for `tools/qf learn`.
- Keep `tools/qf` as CLI wrapper that delegates to Python first for compatibility.
- Preserve existing argument/env surface and gate semantics to avoid workflow breakage.

### Risk / rollback
- Risk: wrapper/implementation drift if both paths evolve independently.
- Mitigation: Python-first path executes by default; Bash body remains compatibility fallback only.
- Rollback: remove delegation line in `cmd_learn` to return to legacy Bash body.

## Incremental decision (make init Python-first, keep Bash as wrapper)
### Why
- You requested to standardize command logic in Python and keep Bash thin.
- `init` is the session entry gate and must be stable, testable, and easy to extend.
- Python implementation makes status computation/output contracts easier to maintain consistently.

### Decision
- Introduce `tools/qf_init.py` as the canonical implementation for `tools/qf init`.
- Keep `tools/qf` as CLI wrapper that delegates to Python first for compatibility.
- Preserve existing `init` flags and outputs (`check`, `-status`, `-main`) with no workflow contract change.

### Risk / rollback
- Risk: temporary divergence if both Python and legacy Bash branches are modified.
- Mitigation: Python path is primary; Bash path remains fallback only.
- Rollback: remove `cmd_init` delegation line to restore legacy Bash-only path.
