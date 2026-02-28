# Sync Report

RUN_ID: `run-2026-03-01-qf-sync-ready`
Generated At (UTC): 2026-02-28T17:38:48.388258+00:00
SYNC_PASS: true

## Files Read
- `README.md` (required, read, lines=45)
- `SYNC/README.md` (required, read, lines=36)
- `SYNC/READ_ORDER.md` (required, read, lines=42)
- `SYNC/CURRENT_STATE.md` (required, read, lines=26)
- `SYNC/SESSION_LATEST.md` (required, read, lines=27)
- `SYNC/DECISIONS_LATEST.md` (required, read, lines=54)
- `SYNC/LINKS.md` (required, read, lines=34)
- `SYNC/EXAM_PLAN_PROMPT.md` (required, read, lines=24)
- `SYNC/EXAM_ANSWER_TEMPLATE.md` (required, read, lines=43)
- `SYNC/EXAM_WORKFLOW.md` (required, read, lines=31)
- `SYNC/EXAM_RUBRIC.json` (required, read, lines=87)
- `AGENTS.md` (required, read, lines=138)
- `docs/WORKFLOW.md` (required, read, lines=162)
- `docs/ENTITIES.md` (required, read, lines=94)
- `docs/PROJECT_GUIDE.md` (required, read, lines=450)
- `TASKS/STATE.md` (required, read, lines=53)
- `TASKS/QUEUE.md` (required, read, lines=254)
- `TASKS/TASK-qf-sync-ready.md` (optional, read, lines=41)
- `reports/run-2026-03-01-qf-sync-ready/handoff.md` (optional, missing, lines=0)
- `reports/run-2026-03-01-qf-sync-ready/conversation.md` (optional, missing, lines=0)
- `reports/run-2026-03-01-qf-sync-ready/decision.md` (optional, read, lines=12)
- `reports/run-2026-03-01-qf-sync-ready/summary.md` (optional, read, lines=12)

## Project Overview
- Summary: quant-factory-os is the governance/execution base for quant engineering.
- North star: quant-factory-os 是一个“自举式智能工厂操作系统”：它能**自动执行任务**、能**从证据链与错题本学习变强**、能**训练/引导新的智能体加入并理解因果链**、能**自我迭代升级工具与流程**、最终能**多智能协作形成涌现智能**，并把这些能力用于任何项目（最初是量化策略工厂，最终是通用项目底座）。

## Governance
- Constitution: `AGENTS.md`
- Workflow: `docs/WORKFLOW.md`
- Entity map: `docs/ENTITIES.md`

## Skill Lookup
- Primary: `AGENTS.md` Skills section
- Fallback: `/root/.codex/skills/.system/*/SKILL.md`

## Current Stage
- CURRENT_RUN_ID: `run-2026-03-01-qf-sync-ready`
- CURRENT_TASK_FILE: `TASKS/TASK-qf-sync-ready.md`
- CURRENT_STATUS: `active`

## Session Continuity
- continuity: `ready_to_continue`
- has_handoff: `false`
- has_decision: `true`
- has_summary: `true`

## Next Command
- `tools/qf ready`

