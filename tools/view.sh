#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: tools/view.sh <path> [--from N] [--to M] [--max-lines K] [--find PATTERN] [--context N]"
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
find_pattern=""
context=0

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
    --find)
      find_pattern="${2:-}"
      shift 2
      ;;
    --context)
      context="${2:-}"
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

is_non_negative_int() {
  [[ "$1" =~ ^[0-9]+$ ]]
}

if [[ -n "$find_pattern" ]]; then
  if [[ -z "$find_pattern" ]]; then
    echo "ERROR: --find requires a non-empty pattern."
    exit 2
  fi
  if ! is_non_negative_int "$context"; then
    echo "ERROR: --context must be a non-negative integer."
    exit 2
  fi
else
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

relative_path="${resolved#"$repo_root"/}"
if [[ "$resolved" == "$repo_root" ]]; then
  relative_path="."
fi

denylist_file="$repo_root/.codex_read_denylist"
if [[ -f "$denylist_file" ]]; then
  matched_pattern=""
  while IFS= read -r raw_line || [[ -n "$raw_line" ]]; do
    line="${raw_line%$'\r'}"
    if [[ "$line" =~ ^[[:space:]]*$ ]] || [[ "$line" =~ ^[[:space:]]*# ]]; then
      continue
    fi

    pattern="${line#"${line%%[![:space:]]*}"}"
    pattern="${pattern%"${pattern##*[![:space:]]}"}"
    [[ -z "$pattern" ]] && continue

    if [[ "$relative_path" == $pattern ]] || [[ "$resolved" == $pattern ]] || [[ "$path" == $pattern ]]; then
      matched_pattern="$pattern"
      break
    fi
  done < "$denylist_file"

  if [[ -n "$matched_pattern" ]]; then
    if [[ "${CODEX_READ_DENYLIST_ALLOW:-0}" == "1" ]]; then
      echo "NOTICE: .codex_read_denylist override enabled (CODEX_READ_DENYLIST_ALLOW=1), matched pattern: $matched_pattern" >&2
    else
      echo "ERROR: blocked by .codex_read_denylist (matched pattern: $matched_pattern)." >&2
      echo "Set CODEX_READ_DENYLIST_ALLOW=1 to override with audit trail." >&2
      exit 1
    fi
  fi
fi

if [[ ! -f "$resolved" ]]; then
  echo "ERROR: path is not a regular file."
  exit 1
fi

if [[ -n "$find_pattern" ]]; then
  if [[ "$context" -gt 0 ]]; then
    set +e
    matches="$(awk -v pat="$find_pattern" -v ctx="$context" '
      $0 ~ pat {
        start = NR - ctx
        end = NR + ctx
        if (start < 1) start = 1
        for (i = start; i <= end; i++) {
          print i
        }
        found = 1
      }
      END {
        if (!found) exit 1
      }
    ' "$resolved" | awk '!seen[$0]++ {print}')"
    rc=$?
    set -e
    if [[ $rc -ne 0 || -z "$matches" ]]; then
      echo "No matches for pattern: $find_pattern"
      exit 1
    fi
    printf "%s\n" "$matches"
  else
    set +e
    matches="$(awk -v pat="$find_pattern" '
      $0 ~ pat {print NR; found=1}
      END { if (!found) exit 1 }
    ' "$resolved")"
    rc=$?
    set -e
    if [[ $rc -ne 0 || -z "$matches" ]]; then
      echo "No matches for pattern: $find_pattern"
      exit 1
    fi
    printf "%s\n" "$matches"
  fi
else
  awk -v start="$from" -v end="$to" 'NR>=start && NR<=end {print}' "$resolved"
fi
