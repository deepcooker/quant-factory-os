#!/usr/bin/env bash
set -euo pipefail

# Backward-compatible wrapper. Canonical entrypoint is: tools/qf onboard <RUN_ID>
exec bash tools/qf onboard "${1:-${RUN_ID:-}}"
