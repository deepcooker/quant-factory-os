# TASK: slice-next: P0: ready 先处理未收尾 run（收尾/抛弃） - evidence and docs alignment

RUN_ID: run-2026-03-02-slice-next-p0-ready-run-evidence-and-docs-alignment
OWNER: <you>
PRIORITY: P1

## Goal
Keep evidence and owner docs aligned with final behavior of this direction.

## Scope (Required)
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `SYNC/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- [ ] owner docs updated in same run when behavior/rules changed
- [ ] tools/qf review STRICT=1 AUTO_FIX=1 passes
- [ ] decision records accepted tradeoffs and residual risks
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- Links / files / references
- If data is needed, specify allowed sample constraints (max rows, time window)

## Steps (Optional)
Suggested approach, if you have one.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks:
- Rollback plan:
