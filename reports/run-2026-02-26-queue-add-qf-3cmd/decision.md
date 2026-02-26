# Decision

RUN_ID: `run-2026-02-26-queue-add-qf-3cmd`

## Why
- 需要将 `tools/qf 三命令收敛` 作为下一枪候选置顶到队列，确保后续会话按统一入口推进。

## Options considered
- 选项 A（采用）：直接按既有 Queue 格式新增一条完整 TODO 项并置顶。
- 选项 B（未采用）：仅修改现有同题项内容，不新增置顶条目；未满足“在顶部加入条目”的执行要求。

## Risks / Rollback
- 风险：同类条目并存可能带来重复领取风险。
- 回滚：删除本次新增的置顶条目即可恢复原队列顺序。
