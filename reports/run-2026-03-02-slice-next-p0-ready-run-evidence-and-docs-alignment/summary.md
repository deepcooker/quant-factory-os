# Summary

RUN_ID: `run-2026-03-02-slice-next-p0-ready-run-evidence-and-docs-alignment`

## What changed
- 修复 `tools/task.sh --next` 队列选取偏差：不再盲选第一个未完成项，改为优先选择 `Slice: run_id=<CURRENT_RUN_ID>` 匹配块，避免多批 slice 混跑时反复拉起旧 `core delivery`。
- 修复 `Picked` 标记逻辑：只标记“实际被选中的 queue block 起始行”，不再误改首个未完成条目。
- 新增回归测试覆盖该行为：`tests/test_task_plan_pick.py::test_task_pick_queue_next_prefers_current_run_slice_block`。
- owner docs 同步更新：
  - `AGENTS.md` 增加 queue pick policy 规则
  - `docs/WORKFLOW.md` 增加 S3 阶段 queue pick 行为说明

## Commands / Outputs
- `make verify`
  - result: `109 passed in 27.79s`
- `QF_ALLOW_RUN_ID_MISMATCH=1 tools/qf review RUN_ID=run-2026-03-02-slice-next-p0-ready-run-core-delivery AUTO_FIX=1 STRICT=1`
  - result: `REVIEW_STATUS: pass`, `REVIEW_BLOCKERS: 0`, `REVIEW_WARNINGS: 0`
- `tools/qf do queue-next`（修复后实测）
  - result: 成功拉起 `TASKS/TASK-slice-next-p0-ready-run-evidence-and-docs-alignment-154517.md`，未再误拉 `core delivery`

## Notes
- 子切片 run（`run-...-evidence-and-docs-alignment`）的 strict review 仍会因缺方向门禁文件报 blocker；方向级 strict gate 在父 run（`run-...-core-delivery`）执行并已通过。
