#!/usr/bin/env bash
set -euo pipefail

# tools/ship.sh v1.0.5 (CN PR body + self-guard FIXED)
# ------------------------------------------------------------
# v1.0.1: 修复 stash_ref 末尾冒号导致 stash pop 失败
# v1.0.2: 刚建 PR 会暂时 no checks reported -> 等待 checks 出现再 watch
# v1.0.3:
#   - PR 描述自动生成（中文：diff 摘要/文件列表/验证方式/合并策略）
#   - auto-merge 已合并时不再重复 merge（减少噪音）
# v1.0.4:
#   - 防误提交：默认禁止“顺带提交 tools/ship.sh”
# v1.0.5:
#   - 修复 v1.0.4 保险丝位置：必须放在 stash pop 之后才看得到改动（必定生效）
# ------------------------------------------------------------

MSG="${1:-}"
if [[ -z "$MSG" ]]; then
  echo "用法：tools/ship.sh \"一句话说明改动\""
  exit 1
fi

extract_pr_section() {
  local body="$1"
  local header="$2"
  echo "$body" | awk -v header="$header" '
    $0 ~ "^## " header "$" {inside=1; print; next}
    inside && $0 ~ "^## " {exit}
    inside {print}
  '
}

build_pr_body_excerpt() {
  local body="$1"
  local task_section evidence_section excerpt=""
  task_section="$(extract_pr_section "$body" "任务文件")"
  evidence_section="$(extract_pr_section "$body" "Evidence paths")"
  if [[ -n "$task_section" ]]; then
    excerpt="$task_section"
  fi
  if [[ -n "$evidence_section" ]]; then
    if [[ -n "$excerpt" ]]; then
      excerpt="${excerpt}

${evidence_section}"
    else
      excerpt="$evidence_section"
    fi
  fi
  printf "%s" "$excerpt"
}

emit_pr_body_excerpt() {
  local run_id="$1"
  local excerpt="$2"
  if [[ -z "$run_id" || -z "$excerpt" ]]; then
    return 0
  fi
  mkdir -p "reports/${run_id}"
  printf "%s\n" "$excerpt" > "reports/${run_id}/pr_body_excerpt.md"
}

wait_for_pr_merged() {
  local pr_url="$1"
  local state=""
  while true; do
    state="$(gh pr view "$pr_url" --json state -q .state || true)"
    if [[ "$state" == "MERGED" ]]; then
      echo "merge confirmed (state=MERGED)"
      break
    fi
    echo "waiting merge... (state=${state:-unknown})"
    sleep 3
  done
}

json_escape() {
  local value="${1:-}"
  value="${value//\\/\\\\}"
  value="${value//\"/\\\"}"
  value="${value//$'\n'/\\n}"
  value="${value//$'\r'/}"
  printf "%s" "$value"
}

ship_state_file=""
current_ship_step=""
RETRY_OUTPUT=""
RETRY_LAST_ERROR=""

classify_mistake_category() {
  local step="${1:-}"
  case "$step" in
    resume_*|sync_*)
      echo "recovery_error"
      ;;
    *_guard_*|*scope*|*single_run*)
      echo "decision_error"
      ;;
    pr_*|push|commit*)
      echo "execution_error"
      ;;
    *)
      echo "execution_error"
      ;;
  esac
}

append_mistake_event() {
  local step="$1"
  local err="${2:-}"
  local source="${3:-runtime}"
  local attempt="${4:-}"
  local category=""
  local file=""
  local attempt_json=""

  [[ -n "${run_id:-}" ]] || return 0

  category="$(classify_mistake_category "$step")"
  file="reports/${run_id}/mistake_log.jsonl"
  mkdir -p "reports/${run_id}"

  if [[ -n "$attempt" ]]; then
    attempt_json=",\"attempt\":\"$(json_escape "$attempt")\""
  fi

  printf '{"ts":"%s","run_id":"%s","category":"%s","step":"%s","source":"%s","error":"%s"%s}\n' \
    "$(date -Iseconds)" \
    "$(json_escape "${run_id}")" \
    "$(json_escape "${category}")" \
    "$(json_escape "${step}")" \
    "$(json_escape "${source}")" \
    "$(json_escape "${err}")" \
    "${attempt_json}" >> "$file"
}

write_ship_state() {
  local step="$1"
  local last_error="${2:-}"
  local branch_val commit_val pr_val msg_val

  [[ -n "${run_id:-}" ]] || return 0

  ship_state_file="reports/${run_id}/ship_state.json"
  mkdir -p "reports/${run_id}"

  branch_val="$(json_escape "${branch:-}")"
  commit_val="$(json_escape "$(git rev-parse --short HEAD 2>/dev/null || true)")"
  pr_val="$(json_escape "${pr_url:-}")"
  msg_val="$(json_escape "${MSG:-}")"
  last_error="$(json_escape "$last_error")"

  cat > "$ship_state_file" <<EOF
{"run_id":"${run_id}","branch":"${branch_val}","commit":"${commit_val}","pr_url":"${pr_val}","step":"$(json_escape "$step")","last_error":"${last_error}","msg":"${msg_val}","updated_at":"$(date -Iseconds)"}
EOF
}

print_resume_cmd() {
  if [[ -n "${run_id:-}" ]]; then
    echo "恢复命令：tools/qf resume RUN_ID=${run_id}"
  fi
}

fail_with_resume() {
  local step="$1"
  local err="${2:-unknown error}"
  write_ship_state "$step" "$err"
  append_mistake_event "$step" "$err" "fail_with_resume"
  echo "❌ ${step} failed: ${err}" >&2
  print_resume_cmd >&2
  exit 1
}

run_with_retry_capture() {
  local step="$1"
  shift
  local max_attempts="${SHIP_RETRY_MAX:-3}"
  local delay="${SHIP_RETRY_BASE_SEC:-1}"
  local attempt=1
  local rc=0
  local output=""

  RETRY_OUTPUT=""
  RETRY_LAST_ERROR=""
  current_ship_step="$step"
  while true; do
    set +e
    output="$("$@" 2>&1)"
    rc=$?
    set -e
    if [[ "$rc" -eq 0 ]]; then
      RETRY_OUTPUT="$output"
      if [[ -n "$output" ]]; then
        printf "%s\n" "$output"
      fi
      write_ship_state "$step" ""
      return 0
    fi

    RETRY_LAST_ERROR="$(printf "%s" "$output" | tail -n 3 | tr '\n' ' ' | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//')"
    write_ship_state "$step" "$RETRY_LAST_ERROR"
    append_mistake_event "$step" "$RETRY_LAST_ERROR" "retry" "$attempt"
    if [[ "$attempt" -ge "$max_attempts" ]]; then
      if [[ -n "$output" ]]; then
        printf "%s\n" "$output" >&2
      fi
      return "$rc"
    fi
    echo "retry[$attempt/$max_attempts] step=$step rc=$rc: ${RETRY_LAST_ERROR:-unknown}" >&2
    sleep "$delay"
    attempt=$((attempt + 1))
    delay=$((delay * 2))
  done
}

cleanup_empty_branch() {
  local candidate_branch="$1"
  local base_ref="${2:-origin/main}"
  local branch_sha base_sha

  [[ -n "$candidate_branch" ]] || return 0
  if ! git show-ref --verify --quiet "refs/heads/${candidate_branch}"; then
    return 0
  fi

  branch_sha="$(git rev-parse "${candidate_branch}" 2>/dev/null || true)"
  base_sha="$(git rev-parse "${base_ref}" 2>/dev/null || true)"
  if [[ -z "$branch_sha" || -z "$base_sha" || "$branch_sha" != "$base_sha" ]]; then
    return 0
  fi

  git checkout "${orig_branch}" >/dev/null 2>&1 || true
  git branch -D "${candidate_branch}" >/dev/null 2>&1 || true
}


queue_mark_done_in_queue() {
  local queue_file="$1"
  local rid="$2"
  local pr_url="$3"

  [[ -z "$rid" ]] && return 0
  [[ -z "$pr_url" ]] && return 0
  [[ -f "$queue_file" ]] || return 0

  local pr_num=""
  if [[ "$pr_url" =~ /pull/([0-9]+) ]]; then
    pr_num="${BASH_REMATCH[1]}"
  fi
  local done_line="Done: PR #${pr_num:-?}, RUN_ID=${rid}"

  # Replace the first matching picked in-progress item:
  # - [>] ... Picked: <rid> ...  ->  - [x] ... Picked: <rid> ...
  # and insert an indented Done line right after, unless already present.
  awk -v rid="$rid" -v doneline="$done_line" '
    BEGIN { done=0 }
    {
      if (!done && $0 ~ /^- \[>\] / && index($0, "Picked: " rid) > 0) {
        done=1
        sub(/^- \[>\] /, "- [x] ")
        print

        # Peek next line to avoid duplicating Done:
        if ((getline nxt) > 0) {
          if (nxt ~ /^[[:space:]]*Done:/) {
            print nxt
          } else {
            print "  " doneline
            print nxt
          }
        } else {
          print "  " doneline
        }
        next
      }
      print
    }
  ' "$queue_file" > "${queue_file}.tmp" && mv "${queue_file}.tmp" "$queue_file"
}

queue_mark_done_commit_push() {
  local queue_file="$1"
  local rid="$2"
  local pr_url="$3"

  queue_mark_done_in_queue "$queue_file" "$rid" "$pr_url"

  # Commit only if queue changed
  if git diff --quiet -- "$queue_file"; then
    return 0
  fi
  git add "$queue_file"
  git commit -m "${rid}: queue done (${pr_url})" >/dev/null
  git push >/dev/null
}

# Test-only mode (no gh / no PR):
#   SHIP_QUEUE_MARK_DONE_ONLY=1
#   SHIP_QUEUE_MARK_DONE_QUEUE_FILE=...
#   SHIP_QUEUE_MARK_DONE_RUN_ID=...
#   SHIP_QUEUE_MARK_DONE_PR_URL=...
if [[ "${SHIP_QUEUE_MARK_DONE_ONLY:-0}" == "1" ]]; then
  queue_file="${SHIP_QUEUE_MARK_DONE_QUEUE_FILE:-TASKS/QUEUE.md}"
  rid="${SHIP_QUEUE_MARK_DONE_RUN_ID:-${RUN_ID:-}}"
  pr_url="${SHIP_QUEUE_MARK_DONE_PR_URL:-}"
  queue_mark_done_in_queue "$queue_file" "$rid" "$pr_url"
  exit 0
fi


if [[ "${SHIP_PR_BODY_EXCERPT_ONLY:-0}" == "1" ]]; then
  run_id="${SHIP_PR_BODY_EXCERPT_RUN_ID:-${RUN_ID:-}}"
  if [[ -z "${SHIP_PR_BODY_EXCERPT_INPUT:-}" ]]; then
    echo "ERROR: SHIP_PR_BODY_EXCERPT_INPUT is required for excerpt-only mode."
    exit 1
  fi
  excerpt="$(build_pr_body_excerpt "$SHIP_PR_BODY_EXCERPT_INPUT")"
  emit_pr_body_excerpt "$run_id" "$excerpt"
  if [[ -n "$excerpt" ]]; then
    printf "%s\n" "$excerpt"
  fi
  exit 0
fi

guard_single_run() {
  if [[ "${SHIP_ALLOW_MULTI_RUN:-0}" == "1" ]]; then
    echo "⚠️  Single-run guard override enabled (SHIP_ALLOW_MULTI_RUN=1)."
    return 0
  fi

  local files=""
  if [[ -n "${SHIP_GUARD_FILE_LIST:-}" ]]; then
    files="${SHIP_GUARD_FILE_LIST}"
  else
    files="$(git diff --cached --name-only || true)"
  fi
  if [[ -z "$files" ]]; then
    return 0
  fi

  local run_prefixes=""
  local task_files=""
  run_prefixes="$(echo "$files" | grep -oE '^reports/run-[^/]+/' | sort -u || true)"
  task_files="$(echo "$files" | grep -oE '^TASKS/TASK-[^/]+\.md$' | sort -u || true)"
  local run_count task_count
  run_count="$(echo "$run_prefixes" | grep -c . || true)"
  task_count="$(echo "$task_files" | grep -c . || true)"

  if [[ "$run_count" -gt 1 || "$task_count" -gt 1 ]]; then
    echo "❌ 检测到多个 RUN_ID 或多个任务文件。"
    echo "   请先清理工作区，确保单任务单 RUN_ID。"
    echo "   Staged files:"
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      echo "   - $line"
    done <<< "$files"
    if [[ "$run_count" -gt 1 ]]; then
      echo "   RUN_ID: $(echo "$run_prefixes" | tr '\n' ' ')"
    fi
    if [[ "$task_count" -gt 1 ]]; then
      echo "   TASKS: $(echo "$task_files" | tr '\n' ' ')"
    fi
    return 1
  fi
}

guard_workflow_changes() {
  local files="$1"
  [[ -z "$files" ]] && return 0

  local workflow_files=""
  workflow_files="$(echo "$files" | grep -E '^\.github/workflows/[^/]+\.(yml|yaml)$' || true)"
  [[ -z "$workflow_files" ]] && return 0

  if [[ "${SHIP_ALLOW_WORKFLOWS:-0}" == "1" ]]; then
    echo "⚠️ Workflow guard override enabled (SHIP_ALLOW_WORKFLOWS=1)."
    return 0
  fi

  echo "❌ 检测到本次提交包含 GitHub Actions workflow 变更。"
  echo "   本仓库默认走 PR + 本地 make verify，不依赖 Actions。"
  echo "   如需本次明确放行，请使用："
  echo "     SHIP_ALLOW_WORKFLOWS=1 tools/ship.sh \"$MSG\""
  echo "   Workflow files:"
  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    echo "   - $file"
  done <<< "$workflow_files"
  return 1
}

extract_task_run_id() {
  local task_file="$1"
  if [[ -z "$task_file" || ! -f "$task_file" ]]; then
    return 0
  fi
  awk '
    {
      line=$0
      sub(/\r$/, "", line)
      if (line ~ /^RUN_ID:[[:space:]]*/) {
        sub(/^RUN_ID:[[:space:]]*/, "", line)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", line)
        if (line != "") {
          print line
          exit
        }
      }
    }
  ' "$task_file"
}

extract_task_scope_paths() {
  local task_file="$1"
  if [[ -z "$task_file" || ! -f "$task_file" ]]; then
    return 0
  fi
  awk '
    BEGIN { in_scope = 0 }
    {
      line=$0
      sub(/\r$/, "", line)
    }
    line ~ /^##[[:space:]]+Scope/ { in_scope = 1; next }
    in_scope && line ~ /^##[[:space:]]+/ { exit }
    in_scope {
      if (line ~ /^[[:space:]]*-[[:space:]]*`[^`]+`[[:space:]]*$/) {
        sub(/^[[:space:]]*-[[:space:]]*`/, "", line)
        sub(/`[[:space:]]*$/, "", line)
        print line
        next
      }
      if (line ~ /^[[:space:]]*-[[:space:]]*[^[:space:]].*$/) {
        sub(/^[[:space:]]*-[[:space:]]*/, "", line)
        gsub(/^[[:space:]]+|[[:space:]]+$/, "", line)
        print line
      }
    }
  ' "$task_file"
}

match_scope_rule() {
  local file="$1"
  local rule="$2"
  [[ -z "$rule" ]] && return 1

  if [[ "$rule" == */ ]]; then
    [[ "$file" == "$rule"* ]]
    return $?
  fi

  if [[ "$rule" == *"*"* || "$rule" == *"?"* || "$rule" == *"["* ]]; then
    [[ "$file" == $rule ]]
    return $?
  fi

  [[ "$file" == "$rule" || "$file" == "$rule/"* ]]
}

validate_scope_gate() {
  local task_file="$1"
  local current_run_id="$2"
  local files="$3"

  if [[ "${SHIP_ALLOW_OUT_OF_SCOPE:-0}" == "1" ]]; then
    echo "⚠️  Scope gate override enabled (SHIP_ALLOW_OUT_OF_SCOPE=1)."
    return 0
  fi

  if [[ -z "$task_file" ]]; then
    echo "❌ Scope gate: missing task file. Use tools/task.sh or set SHIP_TASK_FILE."
    return 1
  fi
  if [[ ! -f "$task_file" ]]; then
    echo "❌ Scope gate: task file not found: $task_file"
    return 1
  fi

  local scope_paths=""
  scope_paths="$(extract_task_scope_paths "$task_file")"
  if [[ -z "$scope_paths" ]]; then
    echo "❌ Scope gate: task file has no valid '## Scope' entries: $task_file"
    echo "   Add bullet paths under '## Scope', e.g. - \`tools/ship.sh\`"
    return 1
  fi

  local violations=""
  while IFS= read -r file; do
    [[ -z "$file" ]] && continue

    local allowed=0
    if [[ "$file" == "$task_file" ]]; then
      allowed=1
    fi
    if [[ "$allowed" -eq 0 && -n "$current_run_id" && "$file" == "reports/${current_run_id}/"* ]]; then
      allowed=1
    fi
    if [[ "$allowed" -eq 0 ]]; then
      case "$file" in
        TASKS/STATE.md|TASKS/QUEUE.md|docs/WORKFLOW.md)
          allowed=1
          ;;
      esac
    fi

    if [[ "$allowed" -eq 0 ]]; then
      while IFS= read -r rule; do
        [[ -z "$rule" ]] && continue
        if match_scope_rule "$file" "$rule"; then
          allowed=1
          break
        fi
      done <<< "$scope_paths"
    fi

    if [[ "$allowed" -eq 0 ]]; then
      violations="${violations}
$file"
    fi
  done <<< "$files"

  if [[ -n "$violations" ]]; then
    echo "❌ Scope gate: out-of-scope staged files detected."
    echo "   Out-of-scope files:"
    while IFS= read -r bad; do
      [[ -z "$bad" ]] && continue
      echo "   - $bad"
    done <<< "$violations"
    echo "   Fix by editing task Scope or unstaging files."
    echo "   Escape hatch (auditable): SHIP_ALLOW_OUT_OF_SCOPE=1"
    return 1
  fi

  return 0
}

resolve_scope_task_file() {
  local files="$1"
  if [[ -n "${SHIP_TASK_FILE:-}" ]]; then
    printf "%s" "${SHIP_TASK_FILE}"
    return 0
  fi

  local task_candidates=""
  task_candidates="$(echo "$files" | grep -E '^TASKS/TASK-[^/]+\.md$' || true)"
  local count
  count="$(echo "$task_candidates" | grep -c . || true)"
  if [[ "$count" -eq 1 ]]; then
    printf "%s" "$task_candidates"
    return 0
  fi
  printf ""
}

run_scope_gate() {
  local files="$1"
  local task_file=""
  task_file="$(resolve_scope_task_file "$files")"

  local gate_run_id="$run_id"
  if [[ -z "$gate_run_id" && -n "$task_file" ]]; then
    gate_run_id="$(extract_task_run_id "$task_file")"
  fi

  validate_scope_gate "$task_file" "$gate_run_id" "$files"
}

if [[ "${SHIP_GUARD_ONLY:-0}" == "1" ]]; then
  files="${SHIP_GUARD_FILE_LIST:-}"
  if ! guard_single_run; then
    exit 1
  fi
  guard_workflow_changes "$files"
  exit $?
fi

if [[ "${SHIP_SCOPE_GATE_ONLY:-0}" == "1" ]]; then
  files="${SHIP_SCOPE_GATE_FILES:-}"
  task_file="${SHIP_SCOPE_GATE_TASK_FILE:-}"
  gate_run_id="${SHIP_SCOPE_GATE_RUN_ID:-$(extract_task_run_id "$task_file")}"
  validate_scope_gate "$task_file" "$gate_run_id" "$files"
  exit $?
fi

if [[ -n "${GH_TOKEN:-}" ]]; then
  if ! gh auth status -h github.com >/dev/null 2>&1; then
    echo "$GH_TOKEN" | gh auth login -h github.com --with-token >/dev/null
  fi
fi

gh auth status -h github.com >/dev/null
git rev-parse --is-inside-work-tree >/dev/null

orig_branch="$(git rev-parse --abbrev-ref HEAD)"

STASH_NAME=""
if ! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git ls-files --others --exclude-standard)" ]]; then
  STASH_NAME="ship-wip-$(date +%Y%m%d-%H%M%S)"
  echo "Detected local changes. Stashing as: $STASH_NAME"
  git stash push -u -m "$STASH_NAME" >/dev/null
fi

ts="$(date +%Y%m%d-%H%M%S)"
slug="$(echo "$MSG" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-+|-+$//g' | cut -c1-40)"
branch="chore/${slug:-update}-${ts}"

git fetch origin
git checkout main >/dev/null 2>&1 || git checkout -b main origin/main
git pull --rebase origin main
git checkout -b "$branch"

# 先把 stash 恢复到新分支上（如果有）
if [[ -n "$STASH_NAME" ]]; then
  echo "Restoring stashed changes onto $branch ..."
  stash_ref="$(git stash list \
    | awk -v name="$STASH_NAME" '$0 ~ name {print $1}' \
    | head -n1 \
    | sed 's/:$//' \
    || true)"
  if [[ -z "$stash_ref" ]]; then
    echo "ERROR: Could not find stash named $STASH_NAME"
    exit 1
  fi

  set +e
  git stash pop --index "$stash_ref"
  rc=$?
  set -e
  if [[ $rc -ne 0 ]]; then
    cat <<EOF2

⚠️ stash pop 未能自动应用（可能有冲突）。
请你手动处理后再继续：

  1) git status
  2) 解决冲突后：git add -A
  3) 然后再运行一次：
     tools/ship.sh "$MSG"

EOF2
    exit 1
  fi
fi

# v1.0.5: 防误提交保险丝（必定生效）—— 放在 stash pop 之后、git add 前
# 若确实要升级 ship，请显式运行：
#   SHIP_ALLOW_SELF=1 tools/ship.sh "chore: 升级 ship 脚本 ..."
if git diff --name-only | grep -qx "tools/ship.sh" && [[ "${SHIP_ALLOW_SELF:-0}" != "1" ]]; then
  echo "❌ 检测到本次改动包含 tools/ship.sh（发货脚本本体）。"
  echo "   为避免误提交，请你："
  echo "   1) 要么撤销对 tools/ship.sh 的改动：git restore tools/ship.sh"
  echo "   2) 要么确认这是有意升级 ship 脚本，然后用："
  echo "      SHIP_ALLOW_SELF=1 tools/ship.sh \"$MSG\""
  cleanup_empty_branch "$branch" "origin/main"
  exit 1
fi

run_id=""
if [[ -n "${SHIP_RUN_ID:-}" ]]; then
  run_id="${SHIP_RUN_ID}"
elif [[ -n "${RUN_ID:-}" ]]; then
  run_id="${RUN_ID}"
else
  run_id="$(echo "$MSG" | grep -oE 'run-[0-9]{4}-[0-9]{2}-[0-9]{2}-[^ ]+' | head -n1 || true)"
fi

if [[ -n "$run_id" ]]; then
  mkdir -p "reports/${run_id}"
fi
write_ship_state "branch_prepared" ""

stage_changes() {
  git add -u

  if [[ -n "${SHIP_TASK_FILE:-}" ]]; then
    git add "${SHIP_TASK_FILE}"
  fi
  if [[ -n "$run_id" ]]; then
    git add "reports/${run_id}"
  fi

  local untracked=""
  untracked="$(git ls-files --others --exclude-standard || true)"
  if [[ -z "$untracked" ]]; then
    return 0
  fi

  while IFS= read -r file; do
    [[ -z "$file" ]] && continue
    if [[ "$file" == reports/run-*/* ]]; then
      continue
    fi
    case "$file" in
      tools/*|tests/*|TASKS/*|docs/*|Makefile|.codex_read_denylist)
        git add "$file"
        ;;
    esac
  done <<< "$untracked"
}

stage_changes

staged_files="$(git diff --cached --name-only || true)"
if ! guard_workflow_changes "$staged_files"; then
  write_ship_state "workflow_guard_failed" "workflow guard failed"
  append_mistake_event "workflow_guard_failed" "workflow guard failed" "guard"
  cleanup_empty_branch "$branch" "origin/main"
  print_resume_cmd
  exit 1
fi

if ! run_scope_gate "$staged_files"; then
  write_ship_state "scope_gate_failed" "scope gate failed"
  append_mistake_event "scope_gate_failed" "scope gate failed" "guard"
  cleanup_empty_branch "$branch" "origin/main"
  print_resume_cmd
  exit 1
fi

if ! guard_single_run; then
  write_ship_state "single_run_guard_failed" "single-run guard failed"
  append_mistake_event "single_run_guard_failed" "single-run guard failed" "guard"
  cleanup_empty_branch "$branch" "origin/main"
  print_resume_cmd
  exit 1
fi

if echo "$staged_files" | grep -qx "project_all_files.txt" \
  && [[ "${SHIP_ALLOW_FILELIST:-0}" != "1" ]]; then
  write_ship_state "filelist_guard_failed" "project_all_files.txt blocked"
  append_mistake_event "filelist_guard_failed" "project_all_files.txt blocked" "guard"
  echo "❌ 检测到本次提交包含 project_all_files.txt。"
  echo "   该文件为本地生成物，默认不纳入 PR。"
  echo "   如需更新，请设置："
  echo "     SHIP_ALLOW_FILELIST=1 tools/ship.sh \"$MSG\""
  cleanup_empty_branch "$branch" "origin/main"
  print_resume_cmd
  exit 1
fi

if git diff --cached --quiet; then
  write_ship_state "no_changes_staged" "No changes staged"
  echo "No changes staged. Nothing to commit."
  echo "You are on branch: $branch"
  cleanup_empty_branch "$branch" "origin/main"
  exit 0
fi

git commit -m "$MSG"
write_ship_state "committed" ""
if ! run_with_retry_capture "push" git push -u origin "$branch"; then
  fail_with_resume "push" "${RETRY_LAST_ERROR:-git push failed}"
fi

# --- 中文 PR 描述自动生成 ---
stat="$(git diff --stat origin/main...HEAD || true)"
files="$(git diff --name-only origin/main...HEAD || true)"
stat_short="$(echo "$stat" | head -n 60)"
files_short="$(echo "$files" | head -n 120)"

PR_BODY="$(cat <<EOF3
## 变更概述
- 由 \`tools/ship.sh v1.0.5\` 自动生成
- 合并策略：Squash
- 说明：CI 通过后自动合并（Auto-merge）

## 变更范围（git diff --stat）
\`\`\`
${stat_short}
\`\`\`

## 涉及文件
\`\`\`
${files_short}
\`\`\`

## 如何验证
- 必须：GitHub Actions 绿灯（required checks）
- 可选（本地）：
  \`\`\`bash
  pytest -q
  \`\`\`

## 风险与回滚
- 风险：
- 回滚：
EOF3
)"
# ----------------------------

prefix=""
if [[ -n "${SHIP_TASK_FILE:-}" || -n "${SHIP_TASK_TITLE:-}" ]]; then
  task_section="## 任务文件"
  if [[ -n "${SHIP_TASK_FILE:-}" ]]; then
    task_section="${task_section}
- 路径：\`${SHIP_TASK_FILE}\`"
  fi
  if [[ -n "${SHIP_TASK_TITLE:-}" ]]; then
    task_section="${task_section}
- 标题：${SHIP_TASK_TITLE}"
  fi
  prefix="$task_section"
fi

if [[ -n "$run_id" ]]; then
  evidence_section="## Evidence paths
\`\`\`
reports/${run_id}/meta.json
reports/${run_id}/summary.md
reports/${run_id}/decision.md
\`\`\`"
  if [[ -n "$prefix" ]]; then
    prefix="${prefix}

${evidence_section}"
  else
    prefix="${evidence_section}"
  fi
fi

if [[ -n "$prefix" ]]; then
  PR_BODY="${prefix}

${PR_BODY}"
fi

PR_BODY_EXCERPT="$(build_pr_body_excerpt "$PR_BODY")"
emit_pr_body_excerpt "$run_id" "$PR_BODY_EXCERPT"





if ! run_with_retry_capture "pr_create" gh pr create --base main --head "$branch" --title "$MSG" --body "$PR_BODY"; then
  fail_with_resume "pr_create" "${RETRY_LAST_ERROR:-gh pr create failed}"
fi
pr_url="$(printf "%s\n" "$RETRY_OUTPUT" | awk '/^https:\/\/github\.com\/.*\/pull\/[0-9]+$/ {print; exit}')"
if [[ -z "$pr_url" ]]; then
  fail_with_resume "pr_create" "could not parse PR URL from gh output"
fi
write_ship_state "pr_created" ""
echo "PR: $pr_url"

# NEW: auto mark queue done (if a matching [>] Picked: <RUN_ID> exists)
if [[ "${SHIP_QUEUE_AUTO_MARK_DONE:-1}" == "1" && -n "$run_id" ]]; then
  queue_mark_done_commit_push "TASKS/QUEUE.md" "$run_id" "$pr_url" || true
fi

# enable auto-merge AFTER pushing the queue-done commit (so the PR includes it)
run_with_retry_capture "pr_merge_auto" gh pr merge --auto --squash --delete-branch "$pr_url" || true


# 如果 auto-merge 已经合并，就不再重复 merge
if ! run_with_retry_capture "pr_state" gh pr view "$pr_url" --json state -q .state; then
  fail_with_resume "pr_state" "${RETRY_LAST_ERROR:-gh pr view failed}"
fi
state="$(printf "%s\n" "$RETRY_OUTPUT" | tail -n1 | tr -d '\r')"
if [[ "$state" != "MERGED" ]]; then
  if ! run_with_retry_capture "pr_merge" gh pr merge --squash --delete-branch "$pr_url"; then
    fail_with_resume "pr_merge" "${RETRY_LAST_ERROR:-gh pr merge failed}"
  fi
fi
wait_for_pr_merged "$pr_url"
write_ship_state "merged" ""

if [[ -n "$PR_BODY_EXCERPT" ]]; then
  printf "%s\n" "$PR_BODY_EXCERPT"
fi

echo "== 下一枪建议 =="
echo "如果 QUEUE 还有 [ ]：运行 tools/task.sh --next"

if [[ -n "$(git status --porcelain)" ]]; then
  write_ship_state "sync_blocked_dirty" "working tree not clean"
  append_mistake_event "sync_blocked_dirty" "working tree not clean" "guard"
  echo "❌ post-ship sync aborted: working tree is not clean."
  echo "   请先处理工作区改动后再同步 main。"
  print_resume_cmd
  exit 1
fi

if ! run_with_retry_capture "sync_checkout_main" git checkout main; then
  fail_with_resume "sync_checkout_main" "${RETRY_LAST_ERROR:-git checkout main failed}"
fi
if ! run_with_retry_capture "sync_pull_main" git pull --rebase origin main; then
  fail_with_resume "sync_pull_main" "${RETRY_LAST_ERROR:-git pull --rebase origin main failed}"
fi
main_sha="$(git rev-parse --short HEAD)"
origin_sha="$(git rev-parse --short origin/main)"
write_ship_state "synced" ""
echo "post-ship synced main@${main_sha} (origin/main@${origin_sha})"

git branch -D "$branch" >/dev/null 2>&1 || true

echo "Done. (started from: $orig_branch)"
