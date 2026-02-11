# TASK: add .codex_read_denylist + enforce in view/find tools

RUN_ID: run-2026-02-11-codex-read-denylist
OWNER: codex
PRIORITY: P1

## Goal
Add a repo-level read denylist and enforce it in read helpers so Codex avoids noisy/default-disallowed files unless an explicit override is set.

## Non-goals
Do not change existing `tools/view.sh` range/find core behavior or shipping workflow.

## Acceptance
- [ ] Add `.codex_read_denylist` at repo root.
- [ ] Default deny + `CODEX_READ_DENYLIST_ALLOW=1` override behavior works as defined.
- [ ] Minimal pytest regression tests cover default deny and override allow.
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-codex-read-denylist/summary.md` and `reports/run-2026-02-11-codex-read-denylist/decision.md`

## Inputs
- `TASKS/_TEMPLATE.md`
- `tools/view.sh`
- `tools/find.sh` (only if file exists)
- `docs/WORKFLOW.md` (`project_all_files.txt` context/index and default PR exclusion rule)

## Steps (Optional)
1. Create task and evidence skeleton.
2. Add `.codex_read_denylist` with `project_all_files.txt` and usage note.
3. Enforce denylist in `tools/view.sh` before file read.
4. Enforce same in `tools/find.sh` if file exists.
5. Add pytest regression tests for deny/override behavior.
6. Run `make verify`.
7. Update evidence and ship task.

## Reading policy
Use `tools/view.sh` by default. If larger ranges are needed, specify exact line range and reason.

## Risks / Rollback
- Risks: denylist matching too broad/narrow for some path forms.
- Rollback plan: revert this run's denylist/tool/test changes and keep prior read behavior.
