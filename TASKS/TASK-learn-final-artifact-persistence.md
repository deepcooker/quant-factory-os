# TASK: learn final artifact persistence

RUN_ID: run-2026-03-07-learn-final-artifact-persistence
PROJECT_ID: project-0
STATUS: deferred

## Goal
修复 `tools/learn.py` / `tools/codex_transport.py` 在真实 `learn -low/-daily` 完整输出后仍未稳定把 `learn/<project_id>.model.json` 与 `learn/<project_id>.model.raw.txt` 落盘的问题，确保 `ready` 能基于严格 gate 稳定通过。

## Scope
- `tools/learn.py`
- `tools/codex_transport.py`
- `tests/`
- `learn/`
- `TASKS/`
- `reports/`
- `docs/WORKFLOW.md`
- `AGENTS.md`

## Acceptance
- [ ] 真实 `learn -low` 结束后稳定产出 `learn/<project_id>.model.json`
- [ ] 真实 `learn -low` 结束后稳定产出 `learn/<project_id>.model.raw.txt`
- [ ] `python3 tools/ready.py` 在完成 learn 后恢复稳定通过
- [ ] 新增或刷新关键回归测试
- [ ] `make verify` 通过
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Resolution
- Deferred by owner decision.
- This remains a post-Automation-1.0 optimization item, not a current automation-completion blocker.
