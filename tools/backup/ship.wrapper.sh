#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${SCRIPT_DIR}/backup/ship.sh"

echo "DEPRECATED: tools/ship.sh has been archived to tools/backup/ship.sh" >&2
exec "${TARGET}" "$@"
