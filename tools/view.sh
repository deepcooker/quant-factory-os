#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: tools/view.sh <path> [--from N] [--to M] [--max-lines K]"
  exit 2
}

if [[ $# -lt 1 ]]; then
  usage
fi

path="$1"
shift

from=1
to=200
max_lines=260

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from)
      from="${2:-}"
      shift 2
      ;;
    --to)
      to="${2:-}"
      shift 2
      ;;
    --max-lines)
      max_lines="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      ;;
    *)
      echo "ERROR: unknown option: $1"
      usage
      ;;
  esac
done

is_positive_int() {
  [[ "$1" =~ ^[0-9]+$ ]] && [[ "$1" -ge 1 ]]
}

if ! is_positive_int "$from" || ! is_positive_int "$to" || ! is_positive_int "$max_lines"; then
  echo "ERROR: --from/--to/--max-lines must be positive integers."
  exit 2
fi

if [[ "$max_lines" -gt 260 ]]; then
  echo "ERROR: --max-lines exceeds 260. 请分段查看"
  exit 1
fi

if [[ "$to" -lt "$from" ]]; then
  echo "ERROR: --to must be >= --from."
  exit 2
fi

range_count=$((to - from + 1))
if [[ "$range_count" -gt "$max_lines" ]]; then
  echo "ERROR: requested range exceeds limit (${range_count} > ${max_lines}). 请分段查看"
  exit 1
fi

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$repo_root" ]]; then
  echo "ERROR: not inside a git repository."
  exit 1
fi

py_bin=""
if command -v python3 >/dev/null 2>&1; then
  py_bin="python3"
elif command -v python >/dev/null 2>&1; then
  py_bin="python"
else
  echo "ERROR: python is required to resolve paths."
  exit 1
fi

resolved="$("$py_bin" - <<'PY' "$path"
import os
import sys
print(os.path.realpath(sys.argv[1]))
PY
)"

case "$resolved" in
  "$repo_root"/*) ;;
  *)
    echo "ERROR: path must be inside repo root."
    exit 1
    ;;
esac

if [[ ! -f "$resolved" ]]; then
  echo "ERROR: path is not a regular file."
  exit 1
fi

awk -v start="$from" -v end="$to" 'NR>=start && NR<=end {print}' "$resolved"
