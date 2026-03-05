# TASK: remove sync entry and migrate SYNC to chatlogs

## Why
- 当前流程把 `SYNC` 逻辑前置在启动入口，和你要求的“`PROJECT_GUIDE` 作为同频核心”冲突。
- 需要把同频入口收敛到 `AGENTS.md + docs/PROJECT_GUIDE.md`，并让流程从 `init -> learn -> ready` 直接闭环。

## Goal
- 去掉 `SYNC` 入口语义和主流程硬依赖；
- 把原 `SYNC/` 迁移到 `chatlogs/`（非入口）；
- 保持 `tools/qf` 主要命令仍可运行并通过测试。

## Scope (allowlist)
- `tools/qf`
- `tools/sync_exam.py`
- `tests/`
- `AGENTS.md`
- `README.md`
- `docs/WORKFLOW.md`
- `docs/PROJECT_GUIDE.md`
- `docs/LEARN_EXAM_RUBRIC.json`
- `docs/LEARN_EXAM_ANSWER_TEMPLATE.md`
- `TASKS/STATE.md`
- `TASKS/QUEUE.md`
- `chatlogs/`

## Non-goals
- 不重写全部历史 `reports/<RUN_ID>/` 产物。
- 不做与“去 sync 化”无关的功能扩展。

## Acceptance
1. `tools/qf init -> learn -> ready` 在默认路径下不再依赖 `SYNC` 目录入口。
2. 讨论态产物路径改为 `chatlogs/discussion/<RUN_ID>/...`（ready/orient/council/drift）。
3. 主流程与 owner 文档不再引用 `SYNC/*` / `chatlogs/sync/*`。
4. `make verify` 通过。
5. `reports/<RUN_ID>/summary.md` 与 `reports/<RUN_ID>/decision.md` 完整记录本次重构决策与风险。

## Verify
- `make verify`

## Evidence
- `reports/<RUN_ID>/meta.json`
- `reports/<RUN_ID>/summary.md`
- `reports/<RUN_ID>/decision.md`
