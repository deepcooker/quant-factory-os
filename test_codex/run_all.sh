#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${ROOT_DIR}/logs"
ART_DIR="${ROOT_DIR}/artifacts"
mkdir -p "${LOG_DIR}" "${ART_DIR}"

RUN_TS="$(date -u +%Y%m%dT%H%M%SZ)"
SUMMARY_FILE="${LOG_DIR}/summary-${RUN_TS}.tsv"

printf "name\texit_code\tseconds\tlog\n" > "${SUMMARY_FILE}"

run_cmd() {
  local name="$1"
  shift
  local log_file="${LOG_DIR}/${RUN_TS}-${name}.log"
  local start end duration rc
  start="$(date +%s)"
  (
    echo "CMD: $*"
    echo "START_UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    "$@"
  ) >"${log_file}" 2>&1
  rc=$?
  end="$(date +%s)"
  duration="$((end - start))"
  printf "%s\t%s\t%s\t%s\n" "${name}" "${rc}" "${duration}" "${log_file}" >> "${SUMMARY_FILE}"
}

run_cmd version codex --version
run_cmd root_help codex --help
run_cmd exec_help codex exec --help
run_cmd review_help codex review --help
run_cmd login_help codex login --help
run_cmd logout_help codex logout --help
run_cmd mcp_help codex mcp --help
run_cmd mcp_list codex mcp list
run_cmd mcp_server_help codex mcp-server --help
run_cmd app_server_help codex app-server --help
run_cmd completion_help codex completion --help
run_cmd completion_bash_head bash -lc "codex completion bash | head -n 30"
run_cmd sandbox_help codex sandbox --help
run_cmd debug_help codex debug --help
run_cmd apply_help codex apply --help
run_cmd resume_help codex resume --help
run_cmd fork_help codex fork --help
run_cmd cloud_help codex cloud --help
run_cmd features_help codex features --help
run_cmd features_list codex features list
run_cmd exec_resume_help codex exec resume --help
run_cmd exec_review_help codex exec review --help

SCHEMA_PATH="${ART_DIR}/echo_schema.json"
cat > "${SCHEMA_PATH}" <<'EOF'
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "status": { "type": "string" },
    "note": { "type": "string" }
  },
  "required": ["status"],
  "additionalProperties": false
}
EOF

run_cmd exec_basic \
  codex --ask-for-approval never exec \
    --sandbox read-only \
    --output-last-message "${ART_DIR}/exec_basic_last_message.txt" \
    "Reply with exactly one line: CODEX_EXEC_BASIC_OK"

run_cmd exec_json_events bash -lc \
  "codex --ask-for-approval never exec --sandbox read-only --json --output-last-message '${ART_DIR}/exec_json_last_message.txt' 'List exactly three top-level files in this repo.' > '${ART_DIR}/exec_json.events.jsonl'"

run_cmd exec_schema \
  codex --ask-for-approval never exec \
    --sandbox read-only \
    --output-schema "${SCHEMA_PATH}" \
    --output-last-message "${ART_DIR}/exec_schema_output.json" \
    "Return JSON with status and note fields only. status must be ok."

run_cmd exec_search_json bash -lc \
  "codex --search --ask-for-approval never exec --sandbox read-only --json --output-last-message '${ART_DIR}/exec_search_last_message.txt' 'Use web search and return one sentence about Codex CLI docs.' > '${ART_DIR}/exec_search.events.jsonl'"

echo "SUMMARY_FILE=${SUMMARY_FILE}"
