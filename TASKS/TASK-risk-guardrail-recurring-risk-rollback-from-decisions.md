# TASK: risk guardrail: recurring risk/rollback from decisions

RUN_ID: run-2026-02-25-risk-guardrail-recurring-risk-rollback-from-decisions
OWNER: <you>
PRIORITY: P1

## Goal
Aggregate recurring risk/rollback signals in recent decisions and add one preventive guardrail task.

## Scope (Required)
- `TASKS/STATE.md`
- `tests/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- Guardrail task is queue-ready
- make verify

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
    
## Queue-ready follow-up task (copy-paste)

- [ ] TODO Title: 消除 TODO_PROPOSAL 污染工作区（plan 输出迁移 / pick 不依赖 proposal）
  Goal: 让 tools/task.sh --plan 不再修改 repo tracked 的 TASKS/TODO_PROPOSAL.md（改为写到 reports/{RUN_ID}/ 或 /tmp），并让 --pick queue-next 不再强制依赖 proposal 文件，减少 “restore/rm/stash” 之类与任务无关的摩擦。
  Scope: `tools/task.sh`, `tests/`, `docs/WORKFLOW.md`, `TASKS/`, `reports/{RUN_ID}/`
  Acceptance:
  - `--plan` 不会让工作区出现 `M TASKS/TODO_PROPOSAL.md`
  - `--pick queue-next` 不要求 proposal 文件存在
  - `make verify` 全绿

