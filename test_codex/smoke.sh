#!/usr/bin/env bash
set -u

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="${ROOT_DIR}/logs"
ART_DIR="${ROOT_DIR}/artifacts"
mkdir -p "${LOG_DIR}" "${ART_DIR}"

TS="$(date -u +%Y%m%dT%H%M%SZ)"
SUMMARY="${LOG_DIR}/smoke-${TS}.tsv"

printf "test\tstatus\texit_code\tnote\tlog\n" > "${SUMMARY}"

record() {
  local test_name="$1"
  local status="$2"
  local rc="$3"
  local note="$4"
  local log_file="$5"
  printf "%s\t%s\t%s\t%s\t%s\n" "${test_name}" "${status}" "${rc}" "${note}" "${log_file}" >> "${SUMMARY}"
}

run_cmd() {
  local test_name="$1"
  shift
  local log_file="${LOG_DIR}/smoke-${TS}-${test_name}.log"
  (
    echo "CMD: $*"
    echo "START_UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    "$@"
  ) >"${log_file}" 2>&1
  local rc=$?
  if [[ ${rc} -eq 0 ]]; then
    record "${test_name}" "PASS" "${rc}" "-" "${log_file}"
  else
    record "${test_name}" "FAIL" "${rc}" "command_failed" "${log_file}"
  fi
}

run_learn_probe() {
  local test_name="learn_probe"
  local log_file="${LOG_DIR}/smoke-${TS}-${test_name}.log"
  local events_file="${ART_DIR}/smoke-${TS}.learn.events.jsonl"
  local last_file="${ART_DIR}/smoke-${TS}.learn.last.txt"

  local rc
  (
    echo "CMD: codex --search --ask-for-approval never exec --sandbox read-only --json --output-last-message ${last_file} 'Reply with exactly: SMOKE_LEARN_OK'"
    echo "START_UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    codex --search --ask-for-approval never exec \
      --sandbox read-only \
      --json \
      --output-last-message "${last_file}" \
      "Reply with exactly: SMOKE_LEARN_OK" \
      > "${events_file}"
  ) >"${log_file}" 2>&1
  rc=$?

  local has_events=0
  local has_thread_started=0
  local has_item_completed=0
  local has_last=0
  local has_expected_last=0

  [[ -s "${events_file}" ]] && has_events=1
  if [[ ${has_events} -eq 1 ]] && grep -q '"type":"thread.started"' "${events_file}"; then
    has_thread_started=1
  fi
  if [[ ${has_events} -eq 1 ]] && grep -q '"type":"item.completed"' "${events_file}"; then
    has_item_completed=1
  fi
  [[ -s "${last_file}" ]] && has_last=1
  if [[ ${has_last} -eq 1 ]] && grep -q "SMOKE_LEARN_OK" "${last_file}"; then
    has_expected_last=1
  fi

  if [[ ${has_events} -eq 1 && ${has_thread_started} -eq 1 && ${has_item_completed} -eq 1 && ${has_last} -eq 1 && ${has_expected_last} -eq 1 ]]; then
    if [[ ${rc} -eq 0 ]]; then
      record "${test_name}" "PASS" "${rc}" "events_and_last_message_valid" "${log_file}"
    else
      record "${test_name}" "PASS_SOFT" "${rc}" "nonzero_exit_but_events_and_last_message_valid" "${log_file}"
    fi
  else
    local note="missing_artifacts_or_invalid_content"
    record "${test_name}" "FAIL" "${rc}" "${note}" "${log_file}"
  fi
}

run_cmd version codex --version
run_cmd login_status codex login status
run_cmd discuss_profile_help codex --sandbox read-only --ask-for-approval never --help
run_cmd execute_profile_help codex --sandbox workspace-write --ask-for-approval on-request --help
run_learn_probe

echo
echo "Smoke Summary: ${SUMMARY}"
if command -v column >/dev/null 2>&1; then
  column -t -s $'\t' "${SUMMARY}"
else
  cat "${SUMMARY}"
fi
echo
echo "Artifacts:"
echo "- logs: ${LOG_DIR}"
echo "- outputs: ${ART_DIR}"

if awk -F '\t' 'NR>1 && $2=="FAIL" {found=1} END{exit found?0:1}' "${SUMMARY}"; then
  exit 1
fi

exit 0
