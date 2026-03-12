#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${SCRIPT_DIR}/backup/legacy.sh"

echo "DEPRECATED: tools/legacy.sh has been archived to tools/backup/legacy.sh" >&2
exec "${TARGET}" "$@"
