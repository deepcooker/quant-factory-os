# TASK: tools/qf 三命令收敛：init/plan/do + git 自愈（sync/retry/resume）+ 临时产物隔离

RUN_ID: run-2026-02-26-tools-qf-init-plan-do-git-sync-retry-resume
OWNER: <you>
PRIORITY: P1

## Goal
将 enter/onboard/task/ship 收敛到一个产品级入口 `tools/qf`，固定为三命令 `init/plan/do`，并补齐 git 自愈与临时产物隔离。

## Scope (Required)
- `tools/`
- `tests/`
- `docs/WORKFLOW.md`
- `TASKS/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- `tools/qf init` 处理 dirty（可恢复 stash）、强制 sync main、执行 doctor/onboard 并输出下一步提示。
- `tools/qf plan [N]` 生成候选且不污染工作区；proposal 落在 `/tmp` 或 `reports/{RUN_ID}/` 并打印路径。
- `tools/qf do queue-next` 在 plan 前置下自动领取任务并输出 `TASK_FILE`/`RUN_ID`/`EVIDENCE_PATH`。
- 关键 git 步骤支持 retry/resume，失败记录写入 `reports/{RUN_ID}/ship_state.json`。
- 临时产物隔离后不再污染工作区，`make verify` 全绿。

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
