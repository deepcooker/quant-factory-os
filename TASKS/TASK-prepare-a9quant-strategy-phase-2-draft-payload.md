# TASK: Prepare a9quant-strategy phase-2 draft payload

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-prepare-a9quant-strategy-phase-2-draft-payload
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Build a draft init-project phase-2 payload for /root/a9quant-strategy from the completed phase-1 evidence, without writing owner docs into the target project yet.

## Scope
- `Summarize the validated evidence into a phase-2 owner-doc payload draft`
- `Do not run --init-project --phase2-json against the target project yet`

## Non-goals

## Acceptance
- [x] A reviewable phase-2 payload draft exists for /root/a9quant-strategy and clearly preserves current risks and unknowns

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
- Prepared a reviewable phase-2 payload draft at `learn/a9quant-strategy_phase2_draft.json`.
- The draft already contains project-specific markdown for `AGENTS.md`, `docs/PROJECT_GUIDE.md`, `docs/WORKFLOW.md`, `docs/ENTITIES.md`, `docs/FILE_INDEX.md`, and `docs/TOOLS_METHOD_FLOW_MAP.md`.
- The draft keeps current risks explicit instead of pretending the target project is already fully clean or fully abstracted.

### Decisions
- Do not execute `--init-project --phase2-json` yet; review the generated payload first.
- If Phase 2 is later approved, the written owner docs must retain the sandbox-credential, proxy-default, and Bitget-specific coupling risks.

### Risks
- The draft is evidence-based but still comes from static inspection and should be reviewed before writing target owner docs.
- Executing the payload now would mutate `/root/a9quant-strategy`, so that step remains intentionally deferred.

### Verification
- Validated the phase-2 writer schema in `tools/appserverclient.py`.
- Generated `learn/a9quant-strategy_phase2_draft.json` with the required phase-2 keys and markdown blocks.

### Next Steps
- Review the payload draft content.
- If approved, use it as the input for the real phase-2 owner-doc write.

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
