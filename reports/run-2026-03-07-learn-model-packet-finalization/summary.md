# Summary

RUN_ID: `run-2026-03-07-learn-model-packet-finalization`

## What changed
- Added app-server final-answer extraction support in [tools/codex_transport.py](/root/quant-factory-os/tools/codex_transport.py) so learn parsing can recover JSON from event streams instead of relying only on `model.raw.txt`.
- Added event-stream fallback in [tools/learn.py](/root/quant-factory-os/tools/learn.py) so `parse_model_output()` can rebuild the model packet from `learn/<project_id>.model.events.jsonl` when the raw file is missing or incomplete.
- Refreshed regression coverage in [tests/test_codex_transport.py](/root/quant-factory-os/tests/test_codex_transport.py) and [tests/test_learn_model_parse.py](/root/quant-factory-os/tests/test_learn_model_parse.py), including duplicate delta handling and events-only recovery.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-03-07-learn-model-packet-finalization`
- `make verify`
- `env PYTHONUNBUFFERED=1 QF_LEARN_LOG_ACTIVE=1 python3 tools/learn.py -daily`
- `env PYTHONUNBUFFERED=1 QF_LEARN_LOG_ACTIVE=1 python3 tools/learn.py -low`
- `python3 tools/ready.py`
- `make verify` passed: `29 passed in 1.45s`
- `python3 tools/ready.py` passed for `run-2026-03-07-learn-model-packet-finalization`

## Notes
- The original blocker was that `ready` could not pass because `learn/project-0.model.json` was not being produced reliably after app-server plan-mode sync.
- One live regression came from duplicate app-server delta streams (`item/agentMessage/delta` and `codex/event/agent_message_content_delta`) causing duplicated final-answer text; this run now ignores the duplicate codex-event deltas when the item-level stream is present.
- Final live validation now closes: `learn/project-0.model.json` and `learn/project-0.model.raw.txt` both landed under the new run context, and `ready.json` was written successfully.
