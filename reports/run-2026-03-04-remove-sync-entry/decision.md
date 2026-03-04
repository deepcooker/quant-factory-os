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

## Risks / Rollback
- Risk: some wording may differ from older docs until full cross-doc pass is completed.
- Rollback: restore previous `AGENTS.md` from git history if this contract is rejected.
- Risk: significant coverage reduction in qf/sync paths; regressions may slip undetected.
- Rollback: restore deleted test files from git history and reintroduce focused cases incrementally.
