# TASK: session denoise and mainline cleanup

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-session-denoise-and-mainline-cleanup
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
总结 foundation 已开始嵌入外部项目的当前状态，清理已完成 queue 噪音，并对主线文档做最小收口。

## Task Summary
- Status: completed

### Key Updates
- 已将当前 active task 从旧的 a9 文档修复 task 切到新的 cleanup task，避免 runtime_state 继续挂在历史修文上下文上。
- 已清理 TASKS/QUEUE.json 中的 completed 噪音项，只保留当前 cleanup 主线项。
- 已删除 TASKS/ 下除当前 cleanup task 之外的旧 task 文件，共清理 237 个历史 task JSON/MD 文件。
- 已补一条最小主线口径：foundation 已开始嵌入外部业务项目做真实 learnbaseline / owner-doc 同频验证，因此本仓文档继续保持业务无关和流程优先。

### Verification
- runtime_state 当前 task 已切到 task-session-denoise-and-mainline-cleanup。
- TASKS/QUEUE.json 当前只保留 cleanup 主线项。
- TASKS/ 目录当前只保留 TASK-session-denoise-and-mainline-cleanup.json/.md 两个 task 文件。
- docs/WORKFLOW.md 与 docs/PROJECT_GUIDE.md 已补最小主线说明，明确基座已开始嵌入外部业务项目验证。


- 已删除 reports/ 下两个旧的非当前 run 目录，只保留当前主线 run 证据与基础 schema/项目目录。
