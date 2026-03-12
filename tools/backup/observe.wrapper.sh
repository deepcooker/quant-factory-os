#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${SCRIPT_DIR}/backup/observe.sh"

echo "DEPRECATED: tools/observe.sh has been archived to tools/backup/observe.sh" >&2
exec "${TARGET}" "$@"
