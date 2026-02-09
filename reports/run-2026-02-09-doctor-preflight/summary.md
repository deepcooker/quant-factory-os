# Summary

RUN_ID: `run-2026-02-09-doctor-preflight`

## What changed
- Added clearer preflight checks in `tools/doctor.sh` for python/pytest, gh auth, and view tool.

## Commands / Outputs
- Verify: `make verify`（已通过）

## Notes
- Why: 降低进入 codex 前的环境摩擦
- What: doctor 使用 Makefile PY 检查 pytest，补充 gh/view 修复提示
