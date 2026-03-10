#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
用法：tools/smoke.sh [RUN_ID=<run-id>] [TASK_FILE=<task-file>]

说明：
- `smoke` 是 ship 前的 release-prep / readiness 检查层。
- 它不执行远端 git / PR / merge；只判断当前 task 是否具备 ship 条件。
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

run_id="${RUN_ID:-}"
task_file="${TASK_FILE:-}"

for arg in "$@"; do
  case "$arg" in
    RUN_ID=*)
      run_id="${arg#RUN_ID=}"
      ;;
    TASK_FILE=*)
      task_file="${arg#TASK_FILE=}"
      ;;
    "")
      ;;
    *)
      echo "ERROR: unknown arg: $arg" >&2
      usage >&2
      exit 1
      ;;
  esac
done

read_runtime_value() {
  local key="$1"
  python3 tools/project_config.py --get "runtime.${key}" 2>/dev/null || true
}

if [[ -z "$run_id" ]]; then
  run_id="$(read_runtime_value "current_run_id")"
fi
if [[ -z "$task_file" ]]; then
  task_file="$(read_runtime_value "current_task_file")"
fi

if [[ -z "$run_id" || -z "$task_file" ]]; then
  echo "ERROR: missing run/task context" >&2
  echo "RUNTIME_STATE_SOURCE: tools/project_config.json -> runtime_state" >&2
  usage >&2
  exit 1
fi

report_dir="reports/${run_id}"
summary_file="${report_dir}/summary.md"
decision_file="${report_dir}/decision.md"
meta_file="${report_dir}/meta.json"
review_json="${report_dir}/drift_review.json"
review_md="${report_dir}/drift_review.md"
smoke_json="${report_dir}/smoke.json"

missing_items=()

add_missing() {
  missing_items+=("$1")
}

json_escape() {
  local value="${1:-}"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  value="${value//$'\n'/\\n}"
  value="${value//$'\r'/}"
  printf "%s" "$value"
}

write_smoke_json() {
  local status="$1"
  local review_status="$2"
  local missing_json="" item first=1
  mkdir -p "$report_dir"
  if [[ "${#missing_items[@]}" -gt 0 ]]; then
    for item in "${missing_items[@]}"; do
      if [[ $first -eq 0 ]]; then
        missing_json+=","
      fi
      first=0
      missing_json+="\"$(json_escape "$item")\""
    done
  fi
  cat > "$smoke_json" <<EOF
{"schema":"qf_smoke.v1","run_id":"$(json_escape "$run_id")","task_file":"$(json_escape "$task_file")","status":"$(json_escape "$status")","drift_review_status":"$(json_escape "$review_status")","missing_items":[${missing_json}],"next_command":"$(json_escape "tools/ship.sh \"<message>\"")","updated_at":"$(date -Iseconds)"}
EOF
}

echo "SMOKE_STEP[1/6]: resolve context"
echo "SMOKE_RUN_ID: ${run_id}"
echo "SMOKE_TASK_FILE: ${task_file}"

echo "SMOKE_STEP[2/6]: check task contract"
if [[ ! -f "$task_file" ]]; then
  add_missing "task_file"
fi

echo "SMOKE_STEP[3/6]: check run evidence files"
[[ -f "$summary_file" ]] || add_missing "summary.md"
[[ -f "$decision_file" ]] || add_missing "decision.md"
[[ -f "$meta_file" ]] || add_missing "meta.json"

echo "SMOKE_STEP[4/6]: check review artifacts"
[[ -f "$review_json" ]] || add_missing "drift_review.json"
[[ -f "$review_md" ]] || add_missing "drift_review.md"

echo "SMOKE_STEP[5/6]: inspect review status"
review_status="missing"
blockers_count=""
if [[ -f "$review_json" ]]; then
  review_status="$(python3 - "$review_json" <<'PY'
import json, sys
from pathlib import Path
obj = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(obj.get("status", "missing"))
PY
)"
  blockers_count="$(python3 - "$review_json" <<'PY'
import json, sys
from pathlib import Path
obj = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(obj.get("blockers_count", ""))
PY
)"
  [[ "$review_status" == "pass" ]] || add_missing "drift_review_status=${review_status}"
  [[ "$blockers_count" == "0" ]] || add_missing "drift_review_blockers=${blockers_count}"
fi
if [[ -f "$summary_file" ]] && ! grep -q "make verify" "$summary_file"; then
  add_missing "verify_record"
fi

echo "SMOKE_STEP[6/6]: write readiness packet"
if [[ "${#missing_items[@]}" -eq 0 ]]; then
  write_smoke_json "pass" "$review_status"
  echo "SMOKE_STATUS: pass"
  echo "SMOKE_MISSING_ITEMS: 0"
  echo "SMOKE_NEXT_COMMAND: tools/ship.sh \"<message>\""
  echo "SMOKE_FILE: ${smoke_json}"
  exit 0
fi

write_smoke_json "fail" "$review_status"
echo "SMOKE_STATUS: fail"
echo "SMOKE_MISSING_ITEMS: ${#missing_items[@]}"
i=1
for item in "${missing_items[@]}"; do
  echo "SMOKE_MISSING_ITEM_${i}: ${item}"
  i=$((i + 1))
done
echo "SMOKE_FILE: ${smoke_json}"
exit 1
