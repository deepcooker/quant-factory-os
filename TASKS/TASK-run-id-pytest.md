# TASK: 修复 <RUN_ID> 占位符渲染 + 忽略 pytest 缓存确保工作区干净

RUN_ID: run-2026-02-24-run-id-pytest
OWNER: <you>
PRIORITY: P1

## Goal
将 repo 中用于文档/队列/模板的 `<RUN_ID>` 占位符替换为 `{RUN_ID}`（或转义为 `&lt;RUN_ID&gt;`），避免 Markdown 渲染吞字符；同时把 `.pytest_cache/` 加入 `.gitignore`，避免 doctor/pytest 造成工作区“脏”。

## Scope (Required)
- `.gitignore`
- `TASKS/QUEUE.md`
- `TASKS/_TEMPLATE.md`
- `docs/WORKFLOW.md`
- `tests/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- GitHub 渲染下不再出现 `reports//`、`RUN_ID=` 这种空洞显示（示例：QUEUE 与模板中的占位符可读）。
- `tools/doctor.sh`（含 pytest）运行后，工作区保持干净（无未忽略的新增缓存文件）。
- `make verify` 全绿。

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
