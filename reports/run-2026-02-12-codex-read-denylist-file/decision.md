# Decision

RUN_ID: `run-2026-02-12-codex-read-denylist-file`

## Why
- `tools/view.sh` denylist checks read `repo_root/.codex_read_denylist`, so this
  file must be a tracked baseline artifact; otherwise behavior can drift per local
  workspace and shipping may fail due to untracked file policy.

## Options considered
- Option A: broaden ship allowlist to include all dotfiles.
- Option B: minimally allow only `.codex_read_denylist` and add controlled file.
- Decision: Option B for least privilege and explicit intent.

## Risks / Rollback
- Risk: denylist contents may become overly broad and block expected reads.
- Rollback: revert `.codex_read_denylist` and `tools/ship.sh` allowlist change.
