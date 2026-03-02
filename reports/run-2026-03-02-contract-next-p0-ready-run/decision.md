# Decision

RUN_ID: `run-2026-03-02-contract-next-p0-ready-run`

## Why
- 本任务目标是把 `ready` 的会话分流与方向契约门禁做最终核验，避免“历史未收尾状态直接污染新需求执行”。

## Options considered
- 方案 A：继续新增流程能力
  - 放弃原因：当前验收点是收口核验，不应扩大变更面。
- 方案 B：对既有实现做证据化核验并收尾（采用）
  - 结果：方向契约存在，严格 review 通过，`make verify` 全绿。

## Risks / Rollback
- 风险：
  - 工作树当前存在多 run 并行证据文件，后续 ship 时需要保持 RUN_ID 一致性和证据归档一致。
- 回滚：
  - 本 run 未新增功能逻辑；若需回退，仅回退本 run 证据文件即可。

## Stop Reason
- task_done
