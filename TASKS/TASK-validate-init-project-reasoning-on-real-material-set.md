# TASK: validate init-project reasoning on real material set

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-validate-init-project-reasoning-on-real-material-set
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Run init-project phase1 against an in-repo real-material-derived project fixture and verify Q1 Q2 Q5 Q6 Q11 remain stable outside the tiny fixture.

## Scope
- `tools/appserverclient.py`
- `fixtures/`
- `learn/`
- `reports/`

## Non-goals

## Acceptance
- [x] A real-material-derived in-repo project fixture returns stable answered_questions for Q1 Q2 Q5 Q6 Q11
- [x] Evidence updated for the validation run

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
- Added `fixtures/init_project_real_material_fixture/` with README, five layered raw docs, and core implementation evidence files.
- Validated `--init-project -new` against the richer fixture and confirmed stable first-round answers for `Q1/Q2/Q5/Q6/Q11`.
- Tightened the Q6 heuristic so README + docs + explicit implementation anchors can produce a stable workflow answer without over-expanding other questions.
- Filtered README command-path examples out of `readme_refs_missing_in_repo`, so foundation tool commands no longer appear as missing repo files.

### Decisions
- Use a richer in-repo real-material-derived fixture for generic init-project reasoning validation rather than pointing validation at external project roots.
- Keep Phase 1 fail-closed: even with five answered questions, `ready_for_doc_write` stays `false` until follow-up reads are completed.

### Risks
- Remaining questions are still conservative by design and need evidence-backed expansion, not broad heuristics.

### Verification
- `python3 tools/init.py` with `project_root` temporarily pointed at `fixtures/init_project_real_material_fixture`
- `python3 tools/appserverclient.py --init-project -new`
- `python3 tools/appserverclient.py --init-project -new` after command-path filtering confirmed `readme_refs_missing_in_repo=[]`
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py`
- `python3 tools/project_config.py` after restoring `project_root` to `/root/quant-factory-os`

### Next Steps
- Continue improving phase1 answered questions only where stable evidence exists.

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
