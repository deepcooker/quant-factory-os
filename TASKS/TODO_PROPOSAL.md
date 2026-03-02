# TODO Proposal

Generated at: 2026-03-02T13:21:30+08:00

## Queue candidates
- id=queue-next (recommended): contract-next: P0: ready 先处理未收尾 run（收尾/抛弃）

## Suggested tasks
- id=suggested-1
  - [ ] TODO Title: contract-first: P0: ready 先处理未收尾 run（收尾/抛弃）
    Goal: 避免把历史中断状态混入新需求，先做生命周期分流。
    Scope: `tools/qf`, `tests/`
    Acceptance:
    - [ ] Confirmed option: ready-exit-resolution
    - [ ] Contract source: reports/run-2026-03-02-qf-ready/direction_contract.json
    - [ ] make verify
- id=suggested-2
  - [ ] TODO Title: follow-up: close actions from run-2026-03-02-qf-v1-l1-do-plan
    Goal: Review reports/run-2026-03-02-qf-v1-l1-do-plan/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-3
  - [ ] TODO Title: follow-up: close actions from run-2026-03-02-qf-ready
    Goal: Review reports/run-2026-03-02-qf-ready/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-4
  - [ ] TODO Title: follow-up: close actions from run-2026-03-01-qf-sync-ready
    Goal: Review reports/run-2026-03-01-qf-sync-ready/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-5
  - [ ] TODO Title: follow-up: close actions from run-2026-02-28-sync-exam-assets-followup
    Goal: Review reports/run-2026-02-28-sync-exam-assets-followup/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-6
  - [ ] TODO Title: follow-up: close actions from run-2026-02-28-qf-resume-pr
    Goal: Review reports/run-2026-02-28-qf-resume-pr/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-7
  - [ ] TODO Title: follow-up: close actions from run-2026-02-28-qf-exam-wrapper-command
    Goal: Review reports/run-2026-02-28-qf-exam-wrapper-command/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-8
  - [ ] TODO Title: follow-up: close actions from run-2026-02-28-qf-exam-auto
    Goal: Review reports/run-2026-02-28-qf-exam-auto/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-9
  - [ ] TODO Title: follow-up: close actions from run-2026-02-27-sync-learning-exam-cli-web
    Goal: Review reports/run-2026-02-27-sync-learning-exam-cli-web/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-10
  - [ ] TODO Title: follow-up: close actions from run-2026-02-27-sync-filename-rollback-keep-chinese-content
    Goal: Review reports/run-2026-02-27-sync-filename-rollback-keep-chinese-content/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-11
  - [ ] TODO Title: risk guardrail: recurring risk/rollback from decisions
    Goal: Aggregate recurring risk/rollback signals in recent decisions and add one preventive guardrail task.
    Scope: `TASKS/STATE.md`, `tests/`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Guardrail task is queue-ready
    - [ ] make verify
- id=suggested-12
  - [ ] TODO Title: follow-up: close actions from run-2026-02-27-sync-entrypoint-layer
    Goal: Review reports/run-2026-02-27-sync-entrypoint-layer/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-13
  - [ ] TODO Title: follow-up: close actions from run-2026-02-27-sync-entrypoint-files-ship
    Goal: Review reports/run-2026-02-27-sync-entrypoint-files-ship/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-14
  - [ ] TODO Title: follow-up: close actions from run-2026-02-27-sync-chinese-entrypoint-naming
    Goal: Review reports/run-2026-02-27-sync-chinese-entrypoint-naming/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-15
  - [ ] TODO Title: follow-up: close actions from run-2026-02-27-ship-runid-normalization
    Goal: Review reports/run-2026-02-27-ship-runid-normalization/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-16
  - [ ] TODO Title: follow-up: close actions from run-2026-02-27-qf-stash-clean-command
    Goal: Review reports/run-2026-02-27-qf-stash-clean-command/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-17
  - [ ] TODO Title: follow-up: close actions from run-2026-02-27-qf-session-handoff-execution-log
    Goal: Review reports/run-2026-02-27-qf-session-handoff-execution-log/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-18
  - [ ] TODO Title: follow-up: close actions from run-2026-02-27-qf-handoff-session-summary-format
    Goal: Review reports/run-2026-02-27-qf-handoff-session-summary-format/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-19
  - [ ] TODO Title: follow-up: close actions from run-2026-02-27-project-guide-sync-first-handoff
    Goal: Review reports/run-2026-02-27-project-guide-sync-first-handoff/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify
- id=suggested-20
  - [ ] TODO Title: follow-up: close actions from run-2026-02-27-p1-qf-low-friction-init-handoff-ready
    Goal: Review reports/run-2026-02-27-p1-qf-low-friction-init-handoff-ready/decision.md and convert pending actions into one concrete queue task.
    Scope: `TASKS/QUEUE.md`, `reports/{RUN_ID}/`
    Acceptance:
    - [ ] Queue item added from recent decision
    - [ ] make verify

## Recent decisions
- reports/run-2026-03-02-qf-v1-l1-do-plan/decision.md
- reports/run-2026-03-02-qf-ready/decision.md
- reports/run-2026-03-01-qf-sync-ready/decision.md
- reports/run-2026-02-28-sync-exam-assets-followup/decision.md
- reports/run-2026-02-28-qf-resume-pr/decision.md
- reports/run-2026-02-28-qf-exam-wrapper-command/decision.md
- reports/run-2026-02-28-qf-exam-auto/decision.md
- reports/run-2026-02-27-sync-learning-exam-cli-web/decision.md
- reports/run-2026-02-27-sync-filename-rollback-keep-chinese-content/decision.md
- reports/run-2026-02-27-sync-entrypoint-layer/decision.md
- reports/run-2026-02-27-sync-entrypoint-files-ship/decision.md
- reports/run-2026-02-27-sync-chinese-entrypoint-naming/decision.md
- reports/run-2026-02-27-ship-runid-normalization/decision.md
- reports/run-2026-02-27-qf-stash-clean-command/decision.md
- reports/run-2026-02-27-qf-session-handoff-execution-log/decision.md
- reports/run-2026-02-27-qf-handoff-session-summary-format/decision.md
- reports/run-2026-02-27-project-guide-sync-first-handoff/decision.md
- reports/run-2026-02-27-p1-qf-low-friction-init-handoff-ready/decision.md
- reports/run-2026-02-27-p1-local-chatlogs-full-session-transcript/decision.md
- reports/run-2026-02-27-p0-sync-state-machine-doc-gates/decision.md
