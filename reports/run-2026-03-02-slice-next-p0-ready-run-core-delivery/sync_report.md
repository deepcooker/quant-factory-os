# Sync Report

RUN_ID: `run-2026-03-02-slice-next-p0-ready-run-core-delivery`
Generated At (UTC): 2026-03-02T07:16:01.901950+00:00
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
- `AGENTS.md` (required, read, lines=162)
- `docs/WORKFLOW.md` (required, read, lines=221)
- `docs/ENTITIES.md` (required, read, lines=94)
- `docs/PROJECT_GUIDE.md` (required, read, lines=450)
- `TASKS/STATE.md` (required, read, lines=104)
- `TASKS/QUEUE.md` (required, read, lines=353)
- `TASKS/TASK-slice-next-p0-ready-run-core-delivery-144925.md` (optional, read, lines=37)
- `reports/run-2026-03-02-slice-next-p0-ready-run-core-delivery/handoff.md` (optional, missing, lines=0)
- `reports/run-2026-03-02-slice-next-p0-ready-run-core-delivery/conversation.md` (optional, read, lines=14)
- `reports/run-2026-03-02-slice-next-p0-ready-run-core-delivery/decision.md` (optional, read, lines=19)
- `reports/run-2026-03-02-slice-next-p0-ready-run-core-delivery/summary.md` (optional, read, lines=14)
- `reports/run-2026-03-02-slice-next-p0-ready-run-core-delivery/orient_choice.json` (optional, missing, lines=0)
- `reports/run-2026-03-02-slice-next-p0-ready-run-core-delivery/direction_contract.json` (optional, missing, lines=0)
- `reports/run-2026-03-02-slice-next-p0-ready-run-core-delivery/execution_contract.json` (optional, missing, lines=0)
- `reports/run-2026-03-02-slice-next-p0-ready-run-core-delivery/slice_state.json` (optional, missing, lines=0)
- `reports/run-2026-03-02-slice-next-p0-ready-run-core-delivery/drift_review.json` (optional, read, lines=62)
- `reports/run-2026-03-02-slice-next-p0-ready-run-core-delivery/drift_review.md` (optional, read, lines=25)
- `SYNC/discussion/run-2026-03-02-slice-next-p0-ready-run-core-delivery/ready_brief.json` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-slice-next-p0-ready-run-core-delivery/ready_brief.md` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-slice-next-p0-ready-run-core-delivery/orient.json` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-slice-next-p0-ready-run-core-delivery/orient.md` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-slice-next-p0-ready-run-core-delivery/council.json` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-slice-next-p0-ready-run-core-delivery/council.md` (optional, missing, lines=0)
- `SYNC/discussion/run-2026-03-02-slice-next-p0-ready-run-core-delivery/drift_todo.md` (optional, missing, lines=0)

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
- CURRENT_RUN_ID: `run-2026-03-02-slice-next-p0-ready-run-core-delivery`
- CURRENT_TASK_FILE: `TASKS/TASK-slice-next-p0-ready-run-core-delivery-144925.md`
- CURRENT_STATUS: `active`

## Session Continuity
- continuity: `ready_to_continue`
- has_handoff: `false`
- has_decision: `true`
- has_summary: `true`

## Next Command
- `tools/qf ready`
- low-friction: `tools/qf ready`

