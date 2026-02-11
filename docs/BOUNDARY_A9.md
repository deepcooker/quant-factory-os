# BOUNDARY A9 (v0)

## A. Repo hard boundaries
- 所有变更必须以 `TASKS/` 下任务文件作为入口，并绑定明确 `RUN_ID`；无任务不得改动代码或文档。【出处：AGENTS.md】
- 每个任务必须产出并维护 `reports/<RUN_ID>/meta.json`、`summary.md`、`decision.md` 作为证据存储。【出处：AGENTS.md】
- 默认仅使用仓库允许命令集执行工作，长文件读取必须通过 `tools/view.sh` 分段查看。【出处：AGENTS.md】
- 禁止提交 secrets 与生产数据，生成物单文件不得超过 5MB，表格输出默认不超过 500 行。【出处：AGENTS.md】

## B. Delivery and verification boundaries
- 流程顺序必须满足：先读任务并确认验收，再 `make evidence`，最小改动实现，`make verify` 通过后更新 evidence，再 ship。【出处：AGENTS.md】
- 交付前验证基线命令为 `make verify`（等价执行 `pytest -q`）。【出处：Makefile】
- 单任务单 RUN_ID：一次 ship 不得混入多个任务文件或多个 `reports/run-*` 命名空间。【出处：tools/ship.sh】
- `tools/task.sh` 会把任务路径与标题注入 PR 描述，ship 必须携带任务上下文。【出处：tools/task.sh】

## C. Handoff hard rules
- 未提交改动对其他 agent 或云端执行不存在，不可作为交接事实。【出处：docs/WORKFLOW.md】
- 交接必须通过 PR 或 commit hash，并在 `reports/<RUN_ID>/` 下提供证据。【出处：docs/WORKFLOW.md】
- 需要保留的本地上下文必须写入结构化证据（`summary.md`/`decision.md`/`MISTAKES/`）或 `TASKS/STATE.md`，不能依赖聊天记录。【出处：docs/WORKFLOW.md】
- 仓库内长期记忆范围仅限 `docs/`、`TASKS/STATE.md`、`reports/<RUN_ID>/decision.md` 与 `MISTAKES/`。【出处：docs/WORKFLOW.md】

## D. Unknown / pending evidence
- 关于“PR #62 已添加入口但缺文件、PR #63 已 merged 但未实际包含 `docs/BOUNDARY_A9.md`”的结论，本文件未内置 PR 级原始证据，需以对应 PR 页面与提交文件列表复核。
- Boundary v0 后续扩展（如外部数据接入、数据库策略、OSS 依赖白名单）尚待独立任务定义与补证。
