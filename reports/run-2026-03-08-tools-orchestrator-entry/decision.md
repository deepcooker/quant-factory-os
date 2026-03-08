# Decision

RUN_ID: `run-2026-03-08-tools-orchestrator-entry`

## Why
- The repo now needs a single Python entrypoint that can run the `tools` pipeline from a normal terminal window while preserving full log visibility.

## Options considered
- Keep using individual scripts only.
- Add one Python orchestrator that wraps the existing scripts with unified logging.

## Chosen
- Add `tools/run_main.py` as the single Python entrypoint.
- Keep existing step scripts unchanged and wrap them through subprocess calls first, instead of rewriting every tool into a shared in-process library.
- Log every child process line into one run-scoped log file so Codex can inspect the resulting execution stream later.
- Keep explicit parameters for steps that are not yet naturally one-click, especially `choose`.
- Freeze the next-stage refactor path in [docs/TOOLS_REFACTOR_BLUEPRINT.md](/root/quant-factory-os/docs/TOOLS_REFACTOR_BLUEPRINT.md) before any large code rewrite.
- Treat the blueprint as a hard constraint document, not a suggestion list.
- Correct the refactor order: stage-first splitting is not allowed as the first cut.
- The first mandatory extraction order is `common helpers -> artifact/state -> logging -> workflow -> entry -> runtime`.
- Start implementation with the helper extraction layer, not with stage splitting.
- Reorganize method numbering and the root method-flow map after helper extraction so the repo shows shared helpers before stage logic.
- For `init`, stop modeling the top level as implementation helpers; make it a business-first preflight gate for automation readiness.
- For `init`, add a root log archive mode via `-log` so future optimization can be driven by log review instead of conversational replay.
- Remove `init` mode branching; `init` should be one business gate, not `-status/-main` variants.

## Risks / Rollback
- Risk: some steps require explicit extra inputs, so the first orchestrator version must expose those inputs instead of pretending the whole chain is parameter-free.
- Rollback: remove the new orchestrator entrypoint and keep direct script usage.
