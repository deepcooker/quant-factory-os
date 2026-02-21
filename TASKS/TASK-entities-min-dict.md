# TASK: upgrade ENTITIES to minimal dictionary (Task/PR/RUN_ID/Evidence/STATE/MISTAKES)

RUN_ID: run-2026-02-12-entities-min-dict
OWNER: codex
PRIORITY: P1

## Goal
Upgrade `docs/ENTITIES.md` into a minimal entity dictionary that only documents
existing repository entities and constraints, then add a STATE entrypoint link.

## Scope (Required)
- `docs/ENTITIES.md`
- `TASKS/STATE.md`

## Non-goals
- Do not change business logic, tooling behavior, or workflow scripts.
- Do not expand ENTITIES into a full process handbook.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- `TASKS/_TEMPLATE.md`
- `docs/ENTITIES.md`
- `TASKS/STATE.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `tools/ship.sh`
- `ISSUES/PLAYBOOK.md`

## Steps (Optional)
1. Create evidence skeleton via `make evidence RUN_ID=<RUN_ID>`.
2. Rewrite `docs/ENTITIES.md` as minimal dictionary for confirmed entities.
3. Add one entrypoint line in `TASKS/STATE.md` linking ENTITIES.
4. Run `make verify`.
5. Update `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
6. Ship with `tools/task.sh` using this task file.

## Reading policy
Use `tools/view.sh` by default. If reading larger files, split by line range.

## Risks / Rollback
- Risks: ambiguous terms (e.g. RUN_ID format, MISTAKES policy) may be under-specified.
- Rollback plan: revert this task's doc-only commit if wording causes confusion.
