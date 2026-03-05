#!/usr/bin/env bash
set -euo pipefail

# Backward-compatible wrapper.
exec bash tools/legacy.sh onboard "${1:-${RUN_ID:-}}"
