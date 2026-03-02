# Sync Report

RUN_ID: `run-2026-03-02-qf-ready`
Generated At (UTC): 2026-03-02T08:19:11.916842+00:00
SYNC_PASS: true

## Files Read
- `README.md` (required, read, lines=45)
- `SYNC/README.md` (required, read, lines=54)
- `SYNC/READ_ORDER.md` (required, read, lines=48)
- `SYNC/CURRENT_STATE.md` (required, read, lines=26)
- `SYNC/SESSION_LATEST.md` (required, read, lines=27)
- `SYNC/DECISIONS_LATEST.md` (required, read, lines=54)
- `SYNC/LINKS.md` (required, read, lines=34)
- `SYNC/EXAM_PLAN_PROMPT.md` (required, read, lines=24)
- `SYNC/EXAM_ANSWER_TEMPLATE.md` (required, read, lines=43)
- `SYNC/EXAM_WORKFLOW.md` (required, read, lines=31)
- `SYNC/EXAM_RUBRIC.json` (required, read, lines=87)
- `AGENTS.md` (required, read, lines=165)
- `docs/WORKFLOW.md` (required, read, lines=223)
- `docs/ENTITIES.md` (required, read, lines=94)
- `docs/PROJECT_GUIDE.md` (required, read, lines=450)
- `TASKS/STATE.md` (required, read, lines=149)
- `TASKS/QUEUE.md` (required, read, lines=455)
- `TASKS/TASK-queue-state-closure-20260302.md` (optional, read, lines=39)
- `reports/run-2026-03-02-qf-ready/handoff.md` (optional, missing, lines=0)
- `reports/run-2026-03-02-qf-ready/conversation.md` (optional, missing, lines=0)
- `reports/run-2026-03-02-qf-ready/decision.md` (optional, missing, lines=0)
- `reports/run-2026-03-02-qf-ready/summary.md` (optional, missing, lines=0)
- `reports/run-2026-03-02-qf-ready/orient_choice.json` (optional, missing, lines=0)
- `reports/run-2026-03-02-qf-ready/direction_contract.json` (optional, missing, lines=0)
- `reports/run-2026-03-02-qf-ready/execution_contract.json` (optional, missing, lines=0)
- `reports/run-2026-03-02-qf-ready/slice_state.json` (optional, missing, lines=0)
- `reports/run-2026-03-02-qf-ready/drift_review.json` (optional, missing, lines=0)
- `reports/run-2026-03-02-qf-ready/drift_review.md` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-qf-ready/ready_brief.json` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-qf-ready/ready_brief.md` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-qf-ready/orient.json` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-qf-ready/orient.md` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-qf-ready/council.json` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-qf-ready/council.md` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-qf-ready/drift_todo.md` (optional, missing, lines=0)

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
- CURRENT_RUN_ID: `run-2026-03-02-queue-state-closure`
- CURRENT_TASK_FILE: `TASKS/TASK-queue-state-closure-20260302.md`
- CURRENT_STATUS: `done`

## Session Continuity
- continuity: `partial_context`
- has_handoff: `false`
- has_decision: `false`
- has_summary: `false`

## Next Command
- `tools/qf ready`
- low-friction: `tools/qf ready`

