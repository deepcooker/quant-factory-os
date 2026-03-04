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
