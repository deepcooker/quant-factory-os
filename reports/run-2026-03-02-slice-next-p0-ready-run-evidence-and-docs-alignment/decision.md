# Decision

RUN_ID: `run-2026-03-02-slice-next-p0-ready-run-evidence-and-docs-alignment`

## Why
- 需要在“证据与文档对齐”切片收口一个真实流程偏差：`--next` 在多批 slice 共存时误选旧未完成项，导致自动化执行反复回到已完成路径。

## Options considered
- 方案 A：仅人工清理 `TASKS/QUEUE.md`，不改脚本
  - 放弃原因：只能临时止血，下一次会重复触发。
- 方案 B：在 `tools/task.sh --next` 固化“按当前 run slice 优先”的规则并补测试（采用）
  - 结果：自动选取路径与 `CURRENT_RUN_ID` 对齐，且回归测试已锁定。

## Risks / Rollback
- 风险：
  - 历史队列存在多批遗留切片，短期仍可能在人工干预下触发复杂态；但 `--next` 误选主路径已修复。
  - 子切片 strict review 与方向级 strict review门禁模型仍需继续保持一致使用习惯（子切片非 strict gate owner）。
- 回滚：
  - 若需回退，恢复 `tools/task.sh` 与 `tests/test_task_plan_pick.py` 本次变更即可，队列行为回到旧逻辑。

## Stop Reason
- task_done
