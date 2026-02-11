# Decision

RUN_ID: `run-2026-02-11-boundary-a9-v0`

## Why
- 

## Options considered
- 

## Risks / Rollback
- 
# Decision
- Codify base vs a9 boundary v0 in `docs/BOUNDARY_A9.md` using only repo evidence.

# Why
- Establishes a clear handoff boundary and reduces coordination noise across agents.

# Verify
- `make verify`

## Outcome / Closure
- PR #62（commit `98c7422`）先行建立了 `TASKS/STATE.md` -> `docs/BOUNDARY_A9.md` 的入口关系。
- PR #64 落地了 fix2 任务与证据材料，但未把 `docs/BOUNDARY_A9.md` 带入变更范围。
- PR #65（commit `b627f89`）专门补交 `docs/BOUNDARY_A9.md`，与 PR #64 共同完成 fix2 目标。
- 拆分归因：ship 流程默认 staging 行为未自动包含 `docs/` 新增文件，触发“任务/evidence 与文档本体”分离提交。
- 审计结论：截至当前 `main` 分支，`docs/BOUNDARY_A9.md` 已存在，Boundary v0 入口不再悬空。
