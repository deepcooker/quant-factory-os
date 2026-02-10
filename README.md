# quant-factory-os

quant-factory-os 是量化工程的工厂底座；策略与实盘代码在 `a9quant-strategy`。

这一页是入口：Quickstart、Workflow 摘要、核心概念、文档索引与排错。

## Quick start

No proxy:

```bash
./tools/start.sh
```

With proxy:

```bash
PROXY_URL=http://127.0.0.1:7890 ./tools/start.sh
```

## Workflow (5 steps)

1. Task: pick or create a task file under `TASKS/`.
2. Evidence: run `make evidence RUN_ID=<RUN_ID>`.
3. Code: implement the smallest change that satisfies the task.
4. Verify: run `make verify` and keep it green.
5. Ship: run `tools/task.sh` and select the task file.

每个 RUN 开始前在 codex 执行 `/status` 并写入 `reports/<RUN_ID>/summary.md`。

## Concepts

- Task: a scoped unit of work tracked as a task file under `TASKS/`.
- PR: the only delivery unit; no direct pushes to `main`.
- RUN_ID: a unique run identifier, recommended 1 PR : 1 RUN_ID.
- Evidence: the run evidence stored under `reports/<RUN_ID>/`.

## Entry points

- `tools/start.sh`: start the environment.
- `tools/doctor.sh`: quick health check before work.
- `tools/task.sh`: task-driven ship (wraps `tools/ship.sh`).
- `tools/ship.sh`: direct ship when you already have a task message.

## Workflow summary

Use tasks to scope changes and keep PRs small.
Use evidence to leave a reproducible trail.
Keep verification green before shipping.
Ship only through the task workflow.

## Evidence layout

- `reports/<RUN_ID>/meta.json`: metadata for the run.
- `reports/<RUN_ID>/summary.md`: what changed, commands, outputs.
- `reports/<RUN_ID>/decision.md`: why/what/verify and risks.

## Repository layout

- `TASKS/`: task queue and individual task files.
- `reports/`: evidence per RUN_ID.
- `docs/`: workflow and domain docs.
- `tools/`: entry scripts.
- `tests/`: guardrails checked by `make verify`.

## Command cheatsheet

`tools/doctor.sh`

`make evidence RUN_ID=<RUN_ID>`

`make verify`

`tools/task.sh`

## Working agreement

Keep changes minimal and scoped to the active task.
Update evidence in the same PR.
Do not bypass the task flow.
Use `make verify` as the gate before ship.
Prefer deterministic scripts over manual steps.

## Docs index

- `AGENTS.md` (hard rules and workflow)
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/INTEGRATION_A9.md`

## Troubleshooting

- Workspace not clean: commit or stash before shipping; `tools/task.sh` will stash when needed.
- `gh` auth: run `gh auth login` and re-try `tools/task.sh`.
- Proxy: export `PROXY_URL=http://127.0.0.1:7890` before `./tools/start.sh`.

## Task file checklist

- Title matches the task.
- RUN_ID matches the current run.
- Goal is 1-3 lines and measurable.
- Acceptance includes `make verify` and evidence updates.

## Evidence checklist

- Summary lists what changed and commands run.
- Decision records why/what/verify and risks.
- Evidence stays within size limits.

## Shipping checklist

- Working tree clean or stashed.
- `make verify` is green.
- Ship through `tools/task.sh`.

## CI expectations

CI runs `make verify` on PRs.
PRs merge only when checks are green.
Avoid direct pushes to `main`.

## Security and data

Never commit secrets.
Never commit production data.
Use synthetic or reduced samples only.
