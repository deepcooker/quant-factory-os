#!/usr/bin/env bash
set -euo pipefail

# Backward-compatible wrapper.
exec bash tools/ops_legacy.sh onboard "${1:-${RUN_ID:-}}"
