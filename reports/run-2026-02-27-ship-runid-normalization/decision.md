# Decision

RUN_ID: `run-2026-02-27-ship-runid-normalization`

## Why
- A previous ship run produced `reports/run-...:/ship_state.json`, proving RUN_ID extraction accepted trailing punctuation from commit message text.
- This breaks path consistency and downstream resume/review ergonomics.

## Options considered
- Option A: only tighten message regex.
  - Risk: `RUN_ID` from env (`SHIP_RUN_ID` / `RUN_ID`) could still include punctuation.
- Option B: add shared normalization and apply to all RUN_ID sources.
  - Chosen: lower risk and single behavior across message/env sources.

## Risks / Rollback
- Risks:
  - Normalization could reject uncommon RUN_ID formats.
- Mitigation:
  - Regex still allows common characters: letters, digits, `.`, `_`, `-`.
  - Added parser tests for known bad/normal patterns.
- Rollback:
  - Revert `tools/ship.sh` and `tests/test_ship_runid_parse.py`.
