#!/usr/bin/env bash
set -euo pipefail

# Backward-compatible wrapper. Canonical entrypoint is: tools/ops onboard <RUN_ID>
exec bash tools/ops onboard "${1:-${RUN_ID:-}}"
