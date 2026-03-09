# TASK: remove templates pivot

RUN_ID: run-2026-03-08-remove-templates-pivot
PROJECT_ID: project-0
STATUS: active

## Goal
删除 `templates/` 路线、`imports/` 内容、相关 project-repo / adoption 文档，以及当前仓库下全部测试文件，明确这条基建方向不再作为当前自动化 1.0 的继续路径。

## Scope
- `templates/`
- `imports/`
- `docs/`
- `TASKS/`
- `reports/`
- `tests/`

## Acceptance
- [x] 删除仓库内全部 `templates/` 文件
- [x] 删除 `imports/` 相关内容
- [x] 删除 `project repo / adoption` 相关文档
- [x] 删除仓库内全部测试文件
- [x] owner docs 不再把 `templates/` 或这组 project-repo 文档作为当前路线输出
- [x] `TASKS/STATE.md` 绑定到本次 task/run
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [x] `make verify` 已执行并记录结果
