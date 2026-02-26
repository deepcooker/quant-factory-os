# Decision

RUN_ID: `run-2026-02-26-tools-qf-init-plan-do-git-sync-retry-resume`

## Why
- 将工作流入口从分散脚本收敛到 `tools/qf init/plan/do`，降低使用复杂度，并补上 ship 失败后的可恢复闭环（retry + `ship_state.json` + `resume`）。

## Options considered
- 方案 A（采用）：新增 `tools/qf` 作为统一入口，同时对 `tools/ship.sh` 做最小关键路径增强（重试 + 状态断点）。
- 方案 B（未采用）：只在 `task.sh`/`ship.sh` 内增加更多子参数，不引入 `tools/qf`；对外认知负担仍高，且不满足“三命令收敛”目标。

## Risks / Rollback
- 风险：`tools/ship.sh` 增加重试后，失败等待时间会增长（指数退避）。
- 风险：`tools/qf do` 当前会重复打印一次 `TASK_FILE/RUN_ID/EVIDENCE_PATH`（透传 + 汇总）。
- 回滚：恢复 `tools/ship.sh` 与 `docs/WORKFLOW.md` 到上个提交，删除 `tools/qf` 与新增测试文件。
