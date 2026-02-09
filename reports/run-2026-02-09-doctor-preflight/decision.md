# Decision

RUN_ID: `run-2026-02-09-doctor-preflight`

## Why
- 降低进入 codex 前的环境摩擦（失败时给出明确修复步骤）

## Options considered
- 保持原有通过路径，仅增强失败信息与一致的 python 解析

## Risks / Rollback
- 风险：对 Makefile PY 解析失败导致提示不准确
- 回滚：恢复原 doctor.sh 行为

## Verify
- `make verify`（已通过）

## Ship status
- 失败：git@github.com SSH 公钥权限不足（fetch origin 时失败）
