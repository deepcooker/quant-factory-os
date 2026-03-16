# quant-factory-os

quant-factory-os is the governance/execution base for quant engineering.

This file is an index only. It does not define workflow rules.

## Quick start

```bash
python3 tools/init.py
```

Proxy:
- `tools/start.sh` 已归档到 `chatlogs/backup/start.sh`；当前正式入口是 `python3 tools/init.py`

## Single source map
- Session entrypoint owner: `AGENTS.md` + `docs/PROJECT_GUIDE.md`
- Hard rules owner: `AGENTS.md`
- Execution workflow owner: `docs/WORKFLOW.md`
- Entity definitions owner: `docs/ENTITIES.md`
- Strategy/vision owner: `docs/PROJECT_GUIDE.md`

## Boundary quick rules
- `README.md` is index-only.
- Rules live in `AGENTS.md`.
- Process/state machine lives in `docs/WORKFLOW.md`.
- Session/讨论草稿 live in `chatlogs/discussion/*` (non-source-of-truth).

## Primary docs
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/PROJECT_GUIDE.md`
- `CODEX_CLI_PLAYBOOK.md`
- `CODEX_CLI_SOURCE_AUDIT.md`
- `docs/LEARN_EXAM_RUBRIC.json`
- `docs/LEARN_EXAM_ANSWER_TEMPLATE.md`

## Repo layout
- `TASKS/`: queue and task contracts
- `reports/`: per-RUN evidence
- `docs/`: canonical docs
- `chatlogs/`: local chat/discussion artifacts
- `tools/`: execution scripts
- `tests/`: guardrail tests

## Standard gates
- `python3 tools/evidence.py --run-id <RUN_ID>`
- `pytest -q`
- `python3 tools/slice.py --run-id <RUN_ID> --day YYYY-MM-DD --symbols A,B --start HH:MM --end HH:MM`
