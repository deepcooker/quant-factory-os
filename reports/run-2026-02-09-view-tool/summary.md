# Summary

RUN_ID: `run-2026-02-09-view-tool`

## What changed
- Added `tools/view.sh` read-only viewer, updated reading policy in AGENTS/TEMPLATE, and added tests.
- Adjusted ship staging/guard to use staged-only checks to avoid blocking on unrelated run artifacts.

## Commands / Outputs
- Verify: `make verify`（已通过）

## Notes
- Why: 降低只读查看权限摩擦
- What: 新增 view.sh + 只读策略 + pytest 覆盖；护栏改为 staged-only
