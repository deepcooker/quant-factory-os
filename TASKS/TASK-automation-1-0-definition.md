# TASK: automation 1.0 definition

RUN_ID: run-2026-03-06-automation-1-0-definition
PROJECT_ID: project-0
STATUS: active

## Goal
把“自动化 1.0”的成功定义正式落到 foundation repo 文档：明确它是面向业务项目交付的单入口目标、基座退后台、1.0 验收到交付为止，以及 foundation repo / business project repo 的分层关系。

## Scope
- `docs/`
- `AGENTS.md`
- `TASKS/`
- `reports/`

## Acceptance
- [ ] `Automation 1.0` 的成功定义形成正式文档
- [ ] 文档与 `ENTITIES / WORKFLOW / PROJECT_GUIDE` 现有术语保持一致
- [ ] 明确 1.0 到交付为止，不把运行迭代闭环算入当前验收
- [ ] 明确 foundation repo 与 business project repo 的分层关系
- [ ] `make verify` 通过
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
