# Project Bootstrap

## Purpose
This document explains how to bootstrap a new project into the experimental line.

## Skeleton mode
Run from `quant-factory-os`:

```bash
python3 scripts/bootstrap_experiment_project.py /tmp/demo-target
```

## What gets created
- `AGENTS.md`
- `project_config.json`
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`
- `.agents/skills/`
- `schemas/`
- `state/`
- `reports/`
- `artifacts/`
- `logs/`

## Minimum truth to fill
- What the project is
- What the project is not
- Current stage
- Next smallest executable goal

## Minimum validation
After bootstrap:
- confirm `project_config.json` parses
- confirm `AGENTS.md`, `docs/PROJECT_GUIDE.md`, `docs/WORKFLOW.md` exist
- confirm `.agents/skills/`, `schemas/`, `state/` directories exist

## Runnable mode
To bootstrap a minimally runnable experiment-line skeleton with core skills:

```bash
python3 scripts/bootstrap_experiment_project.py /tmp/demo-target --with-core-skills
```

This mode additionally:
- fills a non-empty `skills` registry in `project_config.json`
- copies the minimum core skills into `.agents/skills/`
- writes `docs/NEXT_STEPS.md`

## Runtime-bundle mode
To bootstrap a self-verifiable runtime bundle on top of runnable mode:

```bash
python3 scripts/bootstrap_experiment_project.py /tmp/demo-target --with-core-skills --with-runtime-bundle
```

This mode additionally:
- copies the minimum runtime files:
  - `main.py`
  - `app.py`
  - `core/schema_utils.py`
  - `docs/EXPERIMENT_LINE_GATE.md`
  - `tests/run_gate.py`
- copies the minimum schema set needed for the experiment-line runtime bundle
- writes `bootstrap_manifest.json`

## Mode summary
- `skeleton`
  - docs + config + directories only
- `runnable`
  - skeleton + core skills registry + copied core skills + `docs/NEXT_STEPS.md`
- `runtime-bundle`
  - runnable + local runtime files + minimum schemas + manifest + local gate entry
