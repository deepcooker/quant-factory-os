# TASK: project guide mainline reinforcement

RUN_ID: run-2026-03-07-project-guide-mainline-reinforcement
PROJECT_ID: project-0
STATUS: active

## Goal
在不改变题库骨架的前提下，把 `PROJECT_GUIDE.md` 进一步收紧成 `learn` 的高质量提问主课程：让模型通过问题体系反向读取宪法、工作流、实体、证据链与 session continuity，并在漂移时回到题目体系重新答题以拉回主线；同时先备份 `PROJECT_GUIDE_1.0_backup.md`。

## Scope
- `docs/PROJECT_GUIDE.md`
- `docs/PROJECT_GUIDE_1.0_backup.md`
- `docs/WORKFLOW.md`
- `AGENTS.md`
- `learn/`
- `TASKS/`
- `reports/`

## Acceptance
- [ ] 先生成 `docs/PROJECT_GUIDE_1.0_backup.md`
- [ ] `PROJECT_GUIDE.md` 题目主干结构保持不变
- [ ] 只对必要的 `为什么问这题 / 标准答案 / 主线意义 / 查找线索` 做最小同步
- [ ] 文档明确 `PROJECT_GUIDE` 通过高质量提问反向逼模型读取全量 owner docs 与证据
- [ ] 文档明确漂移时应回到 `PROJECT_GUIDE` 问题体系重答，而不是继续闲聊
- [ ] 相关 owner docs 在同一 run 内完成最小同步
- [ ] `make verify` 通过
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
