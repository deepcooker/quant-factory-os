# TASK: business project repo skeleton

RUN_ID: run-2026-03-07-business-project-repo-skeleton
PROJECT_ID: project-0
STATUS: active

## Goal
把自动化 1.0 的下一步收成一个可复用的 business project repo 最小骨架，并定义单入口 `factory.py run` 的 v0 编排边界，让 foundation repo 后续可以稳定承接真实业务项目。

## Scope
- `docs/AUTOMATION_1_0.md`
- `docs/BUSINESS_PROJECT_REPO_V0.md`
- `templates/business_project_repo_v0/`
- `TASKS/`
- `reports/`

## Acceptance
- [x] 明确 business project repo 的最小目录结构、必需材料和单入口边界
- [x] 提供一个可复用的 business project repo v0 模板目录
- [x] 模板包含最小项目宪法、任务状态骨架和单入口脚手架
- [x] `docs/AUTOMATION_1_0.md` 与新文档口径一致
- [x] `make verify` 通过
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
