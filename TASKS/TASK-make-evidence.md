# TASK: 领取任务时自动 make evidence + 打印下一步清单（避免人肉步骤）

RUN_ID: run-2026-02-25-make-evidence
OWNER: <you>
PRIORITY: P1

## Goal
在 tools/task.sh --next 与 --pick queue-next 领取任务时自动生成 reports/{RUN_ID}/ 证据三件套，并打印标准下一步清单；若 evidence 失败则回滚 QUEUE 变更，避免出现 [>] 锁死需要手动修复。

## Scope (Required)
- `tools/task.sh`
- `tests/`
- `docs/WORKFLOW.md`
- `TASKS/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- `tools/task.sh --next` 领取后默认自动执行 make evidence，并输出：TASK_FILE/RUN_ID/EVIDENCE_PATH + “下一步清单”。
- `tools/task.sh --pick queue-next` 同样默认自动 evidence + 下一步清单。
- 若 evidence 失败：QUEUE 不应从 `[ ]` 变为 `[>]`（自动回滚），并给出明确错误提示。
- docs/WORKFLOW.md 补充：领取任务已自动生成 evidence，无需再手动 make evidence。
- `make verify` 全绿。

## Inputs
- Links / files / references
- If data is needed, specify allowed sample constraints (max rows, time window)

## Steps (Optional)
Suggested approach, if you have one.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks:
- Rollback plan:
