# Sync Report

RUN_ID: `run-2026-03-02-qf-ready`
Generated At (UTC): 2026-03-03T16:36:25.831833+00:00
SYNC_PASS: true

## Files Read
- `README.md` (required, read, lines=46)
- `SYNC/README.md` (required, read, lines=62)
- `SYNC/READ_ORDER.md` (required, read, lines=51)
- `SYNC/CURRENT_STATE.md` (required, read, lines=26)
- `SYNC/SESSION_LATEST.md` (required, read, lines=23)
- `SYNC/DECISIONS_LATEST.md` (required, read, lines=29)
- `SYNC/LINKS.md` (required, read, lines=35)
- `SYNC/EXAM_PLAN_PROMPT.md` (required, read, lines=37)
- `SYNC/EXAM_ANSWER_TEMPLATE.md` (required, read, lines=91)
- `SYNC/EXAM_WORKFLOW.md` (required, read, lines=32)
- `SYNC/EXAM_RUBRIC.json` (required, read, lines=193)
- `AGENTS.md` (required, read, lines=221)
- `docs/WORKFLOW.md` (required, read, lines=275)
- `docs/ENTITIES.md` (required, read, lines=110)
- `docs/CODEX_CLI_OPERATION.md` (required, read, lines=65)
- `docs/PROJECT_GUIDE.md` (required, read, lines=523)
- `TASKS/STATE.md` (required, read, lines=204)
- `TASKS/QUEUE.md` (required, read, lines=456)
- `TASKS/TASK-qf-ready.md` (optional, read, lines=43)
- `reports/run-2026-03-02-qf-ready/handoff.md` (optional, read, lines=24)
- `reports/run-2026-03-02-qf-ready/conversation.md` (optional, read, lines=361)
- `reports/run-2026-03-02-qf-ready/decision.md` (optional, read, lines=112)
- `reports/run-2026-03-02-qf-ready/summary.md` (optional, read, lines=279)
- `reports/run-2026-03-02-qf-ready/orient_choice.json` (optional, read, lines=14)
- `reports/run-2026-03-02-qf-ready/direction_contract.json` (optional, read, lines=74)
- `reports/run-2026-03-02-qf-ready/execution_contract.json` (optional, read, lines=67)
- `reports/run-2026-03-02-qf-ready/slice_state.json` (optional, read, lines=10)
- `reports/run-2026-03-02-qf-ready/drift_review.json` (optional, read, lines=62)
- `reports/run-2026-03-02-qf-ready/drift_review.md` (optional, read, lines=25)
- `SYNC/discussion/run-2026-03-02-qf-ready/ready_brief.json` (optional, read, lines=36)
- `SYNC/discussion/run-2026-03-02-qf-ready/ready_brief.md` (optional, read, lines=42)
- `SYNC/discussion/run-2026-03-02-qf-ready/orient.json` (optional, read, lines=121)
- `SYNC/discussion/run-2026-03-02-qf-ready/orient.md` (optional, read, lines=50)
- `SYNC/discussion/run-2026-03-02-qf-ready/council.json` (optional, read, lines=125)
- `SYNC/discussion/run-2026-03-02-qf-ready/council.md` (optional, read, lines=46)
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
- CURRENT_PROJECT_ID: `project-0`
- CURRENT_RUN_ID: `run-2026-03-02-qf-ready`
- CURRENT_TASK_FILE: `TASKS/TASK-qf-ready.md`
- CURRENT_STATUS: `active`

## Session Continuity
- continuity: `ready_to_continue`
- has_handoff: `true`
- has_decision: `true`
- has_summary: `true`

## Next Command
- `tools/qf do queue-next`
- low-friction: `tools/qf execute RUN_ID=run-2026-03-02-qf-ready`

