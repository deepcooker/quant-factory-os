# TASK: knowledge-sync weekly

RUN_ID: run-YYYY-MM-DD-knowledge-sync
OWNER: <you>
PRIORITY: P1

## Goal
Review latest official/product knowledge and repo governance, then update canonical docs so new sessions stay aligned.

## Scope (Required)
- `docs/CHANGELOG_KNOWLEDGE.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `chatlogs/PROJECT_GUIDE.md`
- `TASKS/STATE.md`
- `reports/{RUN_ID}/`

## Non-goals
- No business feature implementation.
- No unrelated refactors.

## Acceptance
- [ ] Knowledge changelog updated with date/source/add/change/deprecate/verify/risks.
- [ ] Any governance/workflow drift corrected in AGENTS/docs.
- [ ] `make verify` green.
- [ ] Evidence updated in `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`.

## Inputs
- Official docs used this cycle
- Previous `docs/CHANGELOG_KNOWLEDGE.md`
- Current `TASKS/STATE.md` and latest `reports/<RUN_ID>/decision.md`

## Steps
1) Review official docs and repo governance files.
2) Record deltas in `docs/CHANGELOG_KNOWLEDGE.md`.
3) Apply minimal governance/doc updates.
4) Run `make verify`.
5) Update evidence and ship.

## Reading policy
Use `tools/view.sh` by default.

## Risks / Rollback
- Risks: stale or conflicting guidance.
- Rollback: revert this task's governance/doc deltas and rerun verify.
