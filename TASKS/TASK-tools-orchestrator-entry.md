# TASK: tools orchestrator entry

RUN_ID: run-2026-03-08-tools-orchestrator-entry
PROJECT_ID: project-0
STATUS: active

## Goal
新增一个 Python 总入口，顺序编排 `tools` 研发流程调用，并提供统一 logging，让普通窗口可以通过单入口执行流程、输出逐行日志，便于 Codex 后续根据日志定位和修复问题。

## Scope
- `tools/`
- `Makefile`
- `docs/WORKFLOW.md`
- `TASKS/`
- `reports/`

## Acceptance
- [x] 新增 Python 总入口脚本
- [x] 总入口能顺序调用现有 `tools` 流程
- [x] 总入口对每个流程有开始/结束/失败日志
- [x] 子流程 stdout/stderr 每一行都被统一日志记录
- [x] 关键方法带简洁注释
- [x] `TASKS/STATE.md` 绑定到本次 task/run
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [x] 至少完成一次可执行验证
