# Decision

RUN_ID: `run-2026-02-11-boundary-a9-v0-fix2`

## Why
- `TASKS/STATE.md` contains Boundary v0 entry (`docs/BOUNDARY_A9.md`) but the target file was missing in repository state.
- PR #62 merged with the STATE entry present, leaving a dangling documentation pointer.
- PR #63 was intended to fix it but the merged commit did not actually include `docs/BOUNDARY_A9.md`.
- Therefore fix2 must explicitly add `docs/BOUNDARY_A9.md` and gate delivery on verification.

## Options considered
- Option 1: Also edit `TASKS/STATE.md` to remove or change the pointer.
  - Rejected: violates minimal-diff goal and does not solve intended Boundary v0 doc completion.
- Option 2: Add only `docs/BOUNDARY_A9.md` plus required task/evidence updates.
  - Selected: directly resolves dangling entry with smallest scoped change.

## Risks / Rollback
- Risk: `docs/BOUNDARY_A9.md` could be omitted from staged files during ship, recreating prior failure mode.
- Mitigation: re-opened file with `tools/view.sh` before verify; acceptance requires PR changed files include `docs/BOUNDARY_A9.md`.
- Verify: `make verify` (passed).
- Rollback: revert this task branch/PR if acceptance fails, then re-run with the same RUN_ID gates.

## Outcome / Closure
- PR #62（commit `98c7422`）先产生了 Boundary v0 入口；PR #63 仍未把目标文档带入提交。
- PR #64 已交付 fix2 的任务与证据，但缺失 `docs/BOUNDARY_A9.md`，无法单独完成关闭。
- PR #65（commit `b627f89`）单文件补齐 `docs/BOUNDARY_A9.md`，与 PR #64 形成完整闭环。
- 拆分原因明确为 ship 的默认 staging 行为：`docs/` 新文件未自动入暂存区，导致首次 PR 漏文件。
- 最终结论：`main` 已包含 `docs/BOUNDARY_A9.md`，`TASKS/STATE.md` 对应入口有效且可追溯。
