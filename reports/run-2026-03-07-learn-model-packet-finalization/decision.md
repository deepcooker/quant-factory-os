# Decision

RUN_ID: `run-2026-03-07-learn-model-packet-finalization`

## Why
- `learn -> ready` is still the hard session gate, so the missing model packet had to be treated as the active blocker before any further implementation work.
- The narrowest safe fix was to harden app-server final-answer extraction and events-based parsing rather than weakening the gate or adding a fallback path.

## Options considered
- Patch `ready` to accept a weaker learn artifact without `model.json`.
- Patch `tools/learn.py` / `tools/codex_transport.py` so the strict gate keeps working under the current app-server event shapes.
- Ignore the gate and continue coding on the previous active task.

Chosen:
- Patch the transport and learn parsing path, keep the strict gate unchanged.

## Risks / Rollback
- Risk: live app-server output is still large, so future ergonomics work may need to reduce prompt verbosity, but the strict gate now closes again under the current transport/event shapes.
- Rollback: revert the changes in [tools/codex_transport.py](/root/quant-factory-os/tools/codex_transport.py), [tools/learn.py](/root/quant-factory-os/tools/learn.py), [tests/test_codex_transport.py](/root/quant-factory-os/tests/test_codex_transport.py), and [tests/test_learn_model_parse.py](/root/quant-factory-os/tests/test_learn_model_parse.py).

## Stop Reason
- needs_human_decision
