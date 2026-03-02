# TASK: qf 做强模式 v1：L1方向层 + do/plan 稳定性修复 + 文档强门禁

RUN_ID: run-2026-03-02-qf-v1-l1-do-plan
OWNER: <you>
PRIORITY: P1

## Goal
把 `ready->plan->do` 升级为“先方向确认后执行”的做强模式入口，并修复 `do/plan` 的低摩擦稳定性问题。

## Scope (Required)
- `tools/qf`
- `tests/`
- `docs/WORKFLOW.md`
- `AGENTS.md`
- `SYNC/`
- `TASKS/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- [ ] 新增 L1 方向层入口（`orient/choose` 或等价命令）：基于 `docs/PROJECT_GUIDE.md` + `docs/*` + state/evidence 生成多方向候选与优先级，并落证据文件。
- [ ] `tools/qf do queue-next` 不再因内部日志写入导致 pull 前工作区变脏；失败时仍保留可恢复命令。
- [ ] `tools/qf do` 的 auto-plan 与 pick 链路修复：内部自动 plan 后能继续 pick，不再出现“proposal missing”断链。
- [ ] Queue 为空时提供“回到方向层确认”的明确下一步，不是直接死路。
- [ ] `make verify` 通过；owner 文档（`AGENTS.md`/`docs/WORKFLOW.md`/`SYNC/*`）与本 RUN evidence 同步更新。

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
