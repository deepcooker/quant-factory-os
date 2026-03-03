# TASK: docs governance cleanup: 同频文档全量清理与边界重定义

RUN_ID: run-2026-03-04-docs-governance-cleanup
OWNER: <you>
PRIORITY: P1

## Goal
统一 AGENTS/README/docs/SYNC 的职责边界，删除噪声与重复，细化同频标准，形成可执行且可审计的文档体系。

## Scope (Required)
- `AGENTS.md`
- `README.md`
- `docs/`
- `SYNC/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- [ ] 形成“保留/删除/合并/细化”清单并落地到文档
- [ ] 明确并写入边界规则：哪个问题归哪个 owner 文档
- [ ] 同频入口读序与考试问答保持一致，无冲突项
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

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
