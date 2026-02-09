# Summary

RUN_ID: `run-2026-02-09-ship-echo-prbody`

## What changed
- Added PR body excerpt extraction/output and archiving in `tools/ship.sh`, plus a guardrail test.

## Commands / Outputs
- Verify: `make verify`（已通过）

## Notes
- Why: 避免再请求读取 PR body（自动输出摘要）
- What: ship.sh 提取任务/证据段 + 写入 `reports/$RUN_ID/pr_body_excerpt.md` + 测试
