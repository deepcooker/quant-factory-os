# TASK: simplify init-project to session-first flow

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-simplify-init-project-to-session-first-flow
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Remove init-project special-case heuristics and gates, keep only bootstrap state, init session, xhigh plan prompt flow, resume/update/complete semantics.

## Scope
- `tools/appserverclient.py`
- `tools/project_config.py`
- `tools/prompts/init_project_prompt.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `AGENTS.md`

## Non-goals

## Acceptance
- [x] Command(s) pass: `python3 -m py_compile tools/appserverclient.py tools/project_config.py tools/init.py`
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

## Inputs

## Role Threads
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=optional, thread_id=(none)

## Test Gate
- Status: pending
- Owner role: test

### Required Axes
- functional
- flow
- data
- non_functional

### Evidence

### Blocking Issues

## Role Summaries
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=optional, thread_id=(none)

## Task Summary
- Status: completed

### Key Updates
- removed init-project project-specific question heuristics from phase 1
- removed the old `--phase2-json` writing path from the formal runtime surface
- simplified init-project to session-first `xhigh` plan flow with explicit `--update-init-project` / `--complete-init-project`

### Decisions
- keep only `bootstrap_state` and `init_project_session` as hard init-project state
- let the generic prompt/session contract drive 17-question understanding instead of appserverclient hardcoded project semantics
- do not treat owner-doc writing as part of the formal init-project runtime contract in this repo

### Risks
- phase 1 still depends on manual payload updates rather than a real app-server init thread
- historical task/evidence files still preserve earlier phase2 terminology as audit history

### Verification
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py tools/init.py`
- `python3 tools/project_config.py`

### Next Steps
- continue improving init-project only through generic prompt-driven session reasoning

### Conflict Policy
- Priority order: run-main, test, arch, dev
- Merge rule: append_dedup
- Escalation rule: if conflict remains, escalate to run-main

### Gap Summary

### Escalation Policy
- must_escalate_if: run-main summary missing
- must_escalate_if: test_gate not passed
- must_escalate_if: blocking issue remains
- can_resolve_in_task_if: only dev/arch detail alignment
- can_resolve_in_task_if: no blocking issue
- can_resolve_in_task_if: test gate already passed

### Escalation Summary
- needs_run_main: false

### Run-Main Resolution Policy
- must_confirm_if: escalation_summary.needs_run_main
- can_close_if: run-main summary exists
- can_close_if: test_gate passed
- can_close_if: no blocking issue remains

### Run-Main Resolution
- status: pending_ack
- close_escalation: false

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
