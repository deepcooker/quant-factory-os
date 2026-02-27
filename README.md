# quant-factory-os

quant-factory-os is the governance/execution base for quant engineering.

This file is an index only. It does not define workflow rules.

## Quick start

```bash
./tools/start.sh
```

Proxy:

```bash
PROXY_URL=http://127.0.0.1:7890 ./tools/start.sh
```

## Single source map
- Session entrypoint owner: `SYNC/READ_ORDER.md`
- Hard rules owner: `AGENTS.md`
- Execution workflow owner: `docs/WORKFLOW.md`
- Entity definitions owner: `docs/ENTITIES.md`
- Strategy/vision owner: `docs/PROJECT_GUIDE.md`

## Primary docs
- `SYNC/README.md`
- `SYNC/READ_ORDER.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/PROJECT_GUIDE.md`

## Repo layout
- `TASKS/`: queue and task contracts
- `reports/`: per-RUN evidence
- `docs/`: canonical docs
- `SYNC/`: cross-session handoff entry layer
- `tools/`: execution scripts
- `tests/`: guardrail tests

## Standard gates
- `make evidence RUN_ID=<RUN_ID>`
- `make verify`
- `tools/task.sh`
