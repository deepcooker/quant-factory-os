# TASK: learn model packet finalization

RUN_ID: run-2026-03-07-learn-model-packet-finalization
PROJECT_ID: project-0
STATUS: active

## Goal
修复 `tools/learn.py` / `tools/codex_transport.py` 在 app-server 真实 plan 同频后未稳定落出 `learn/<project_id>.model.json` 的问题，确保 `ready` 能基于有效 model packet 继续通过。

## Scope
- `tools/learn.py`
- `tools/codex_transport.py`
- `learn/`
- `tests/`
- `TASKS/`
- `reports/`
- `docs/`

## Acceptance
- [ ] app-server final-answer 事件可稳定产出可解析的 learn model packet
- [ ] `learn/<project_id>.model.json` 在真实 `learn` 运行后稳定落盘
- [ ] `python3 tools/ready.py` 在完成 `learn` 后恢复通过
- [ ] 新增或刷新关键回归测试
- [ ] `make verify` 通过
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
