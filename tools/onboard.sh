#!/usr/bin/env bash
set -euo pipefail

run_id="${1:-${RUN_ID:-}}"
if [[ -z "$run_id" ]]; then
  echo "ERROR: RUN_ID is required. Usage: tools/onboard.sh <RUN_ID>" >&2
  exit 2
fi

repo_root="${ONBOARD_REPO_ROOT:-.}"
reports_dir="${ONBOARD_REPORTS_DIR:-${repo_root}/reports}"
out_dir="${ONBOARD_OUT_DIR:-${reports_dir}/${run_id}}"
out_file="${out_dir}/onboard.md"
state_file="${ONBOARD_STATE_FILE:-${repo_root}/TASKS/STATE.md}"
queue_file="${ONBOARD_QUEUE_FILE:-${repo_root}/TASKS/QUEUE.md}"
decisions_glob="${ONBOARD_DECISIONS_GLOB:-${reports_dir}/run-*/decision.md}"
recent_limit="${ONBOARD_RECENT_LIMIT:-8}"

mkdir -p "$out_dir"

tmp_recent="$(mktemp)"
cleanup() {
  rm -f "$tmp_recent"
}
trap cleanup EXIT

{
  # shellcheck disable=SC2086
  ls -1t ${decisions_glob} 2>/dev/null | head -n "${recent_limit}" > "$tmp_recent" || true
}

{
  echo "# Session Onboard"
  echo
  echo "RUN_ID: \`${run_id}\`"
  echo "Generated At: $(date -Iseconds)"
  echo
  echo "## 宪法/硬规则入口"
  echo "- AGENTS.md"
  echo
  echo "## 项目背景/阶段入口"
  echo "- PROJECT_GUIDE.md"
  echo
  echo "## 工作流入口"
  echo "- docs/WORKFLOW.md"
  echo "- TASKS/STATE.md"
  echo "- TASKS/QUEUE.md"
  echo
  echo "## 强制复述模板入口"
  echo "- PROJECT_GUIDE.md#强制复述模板"
  echo
  echo "## 最近 decision 入口列表"
  if [[ -s "$tmp_recent" ]]; then
    while IFS= read -r item; do
      [[ -z "$item" ]] && continue
      rel="${item#${repo_root}/}"
      echo "- ${rel}"
    done < "$tmp_recent"
  else
    echo "- 无（未检出 reports/run-*/decision.md）"
  fi
  echo
  echo "## 快速检查"
  if [[ -f "$state_file" ]]; then
    echo "- STATE: ${state_file#${repo_root}/}"
  else
    echo "- STATE: missing (${state_file})"
  fi
  if [[ -f "$queue_file" ]]; then
    echo "- QUEUE: ${queue_file#${repo_root}/}"
  else
    echo "- QUEUE: missing (${queue_file})"
  fi
} | tee "$out_file"

echo "ONBOARD_FILE: $out_file"
