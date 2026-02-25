#!/usr/bin/env bash
set -euo pipefail

# tools/task.sh v0.5
# - 自动将任务路径写入 PR 描述
# - PR 描述由 task.sh 自动生成，和 PR 模板不重复，互补
# - 修复交互选择路径污染问题（仅改此问题，其他逻辑不变）

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

if [[ ! -d "TASKS" ]]; then
  echo "❌ 找不到 TASKS/ 目录（请先创建或同步）"
  exit 1
fi

slugify() {
  local text="$1"
  local slug
  slug="$(echo "$text" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-+|-+$//g')"
  if [[ -z "$slug" ]]; then
    slug="task"
  fi
  echo "$slug"
}

task_plan_generate() {
  local n_raw="${1:-20}"
  local n
  if [[ "$n_raw" =~ ^N=([0-9]+)$ ]]; then
    n="${BASH_REMATCH[1]}"
  elif [[ "$n_raw" =~ ^[0-9]+$ ]]; then
    n="$n_raw"
  else
    n="20"
  fi
  if [[ -z "$n" || "$n" -le 0 ]]; then
    n="20"
  fi

  local queue_file reports_dir proposal_file state_file mistakes_dir
  queue_file="${TASK_PLAN_QUEUE_FILE:-${TASK_BOOTSTRAP_QUEUE_FILE:-TASKS/QUEUE.md}}"
  reports_dir="${TASK_PLAN_REPORTS_DIR:-reports}"
  proposal_file="${TASK_PLAN_OUTPUT_FILE:-TASKS/TODO_PROPOSAL.md}"
  state_file="${TASK_PLAN_STATE_FILE:-TASKS/STATE.md}"
  mistakes_dir="${TASK_PLAN_MISTAKES_DIR:-MISTAKES}"

  if [[ ! -f "$queue_file" ]]; then
    echo "❌ QUEUE 文件不存在：$queue_file"
    exit 1
  fi

  local queue_tmp decision_tmp suggestions_tmp
  queue_tmp="$(mktemp)"
  decision_tmp="$(mktemp)"
  suggestions_tmp="$(mktemp)"
  trap 'rm -f "$queue_tmp" "$decision_tmp" "$suggestions_tmp"' RETURN

  awk '
    /^- \[ \] / {
      line=$0
      sub(/^- \[ \][[:space:]]*TODO Title:[[:space:]]*/, "", line)
      sub(/^- \[ \][[:space:]]*/, "", line)
      gsub(/[[:space:]]+$/, "", line)
      if (line != "") print line
    }
  ' "$queue_file" > "$queue_tmp"

  if [[ -d "$reports_dir" ]]; then
    find "$reports_dir" -maxdepth 2 -type f -name "decision.md" \
      | sort -r > "$decision_tmp"
  fi

  : > "$suggestions_tmp"
  add_suggestion() {
    local title="$1"
    local goal="$2"
    local scope="$3"
    local acceptance="$4"
    local exists
    title="$(echo "$title" | tr '\t' ' ' | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//')"
    goal="$(echo "$goal" | tr '\t' ' ' | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//')"
    scope="$(echo "$scope" | tr '\t' ' ' | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//')"
    acceptance="$(echo "$acceptance" | tr '\t' ' ' | sed -E 's/[[:space:]]+/ /g; s/^ //; s/ $//')"
    [[ -z "$title" ]] && return
    exists="$(awk -F '\t' -v t="$title" '$1==t {print "1"; exit}' "$suggestions_tmp")"
    if [[ -n "$exists" ]]; then
      return
    fi
    printf '%s\t%s\t%s\t%s\n' "$title" "$goal" "$scope" "$acceptance" >> "$suggestions_tmp"
  }

  while IFS= read -r decision_path; do
    [[ -z "$decision_path" ]] && continue
    local decision_run
    decision_run="$(basename "$(dirname "$decision_path")")"
    add_suggestion \
      "follow-up: close actions from ${decision_run}" \
      "Review ${decision_path} and convert pending actions into one concrete queue task." \
      "\`TASKS/QUEUE.md\`, \`reports/{RUN_ID}/\`" \
      "[ ] Queue item added from recent decision;[ ] make verify"

    if awk 'BEGIN{IGNORECASE=1; found=0} /risk|rollback/ {found=1} END{exit(found?0:1)}' "$decision_path"; then
      add_suggestion \
        "risk guardrail: recurring risk/rollback from decisions" \
        "Aggregate recurring risk/rollback signals in recent decisions and add one preventive guardrail task." \
        "\`TASKS/STATE.md\`, \`tests/\`, \`reports/{RUN_ID}/\`" \
        "[ ] Guardrail task is queue-ready;[ ] make verify"
    fi
  done < "$decision_tmp"

  if [[ -f "$state_file" ]] && awk 'BEGIN{IGNORECASE=1; found=0} /risk|todo|next|block|pending/ {found=1} END{exit(found?0:1)}' "$state_file"; then
    add_suggestion \
      "state cleanup: convert open state risks into queued tasks" \
      "Extract open risks/todos from ${state_file} and queue the top actionable item." \
      "\`TASKS/STATE.md\`, \`TASKS/QUEUE.md\`, \`reports/{RUN_ID}/\`" \
      "[ ] One state-driven task queued;[ ] make verify"
  fi

  if [[ -d "$mistakes_dir" ]]; then
    local mistake_count
    mistake_count="$(find "$mistakes_dir" -maxdepth 1 -type f -name "*.md" | wc -l | tr -d ' ')"
    if [[ "${mistake_count:-0}" -gt 0 ]]; then
      add_suggestion \
        "mistake recurrence: add fix-forward guardrail task" \
        "Scan ${mistakes_dir}/*.md for recurring failures and queue one preventative task with a test guardrail." \
        "\`MISTAKES/\`, \`tests/\`, \`TASKS/QUEUE.md\`" \
        "[ ] Recurring issue converted to actionable queue task;[ ] make verify"
    fi
  fi

  # Fallback seeds so `--plan` remains actionable even when queue is empty.
  add_suggestion \
    "workflow polish: tighten queue item acceptance wording" \
    "Normalize one queue item's Acceptance bullets to be testable and deterministic." \
    "\`TASKS/QUEUE.md\`, \`TASKS/_TEMPLATE.md\`" \
    "[ ] Acceptance bullets are machine-checkable;[ ] make verify"
  add_suggestion \
    "evidence hygiene: add missing verify commands to summaries" \
    "Backfill missing verify command records in recent run summaries." \
    "\`reports/{RUN_ID}/summary.md\`, \`reports/{RUN_ID}/decision.md\`" \
    "[ ] Verify commands recorded;[ ] make verify"
  add_suggestion \
    "tests hardening: add regression test for latest workflow change" \
    "Add one focused regression test around the newest workflow behavior." \
    "\`tests/\`, \`tools/\`" \
    "[ ] New regression test fails-before/passes-after;[ ] make verify"
  add_suggestion \
    "state snapshot: refresh TASKS/STATE.md with current blockers" \
    "Refresh current risks/blockers and next-shot ordering in state snapshot." \
    "\`TASKS/STATE.md\`, \`reports/{RUN_ID}/decision.md\`" \
    "[ ] State snapshot aligns with latest decisions;[ ] make verify"
  add_suggestion \
    "docs sync: align WORKFLOW with current task/ship behavior" \
    "Update workflow docs to match current task pickup and ship expectations." \
    "\`docs/WORKFLOW.md\`, \`tests/\`" \
    "[ ] Docs updated with matching guardrail test;[ ] make verify"

  mkdir -p "$(dirname "$proposal_file")"
  {
    echo "# TODO Proposal"
    echo
    echo "Generated at: $(date -Iseconds)"
    echo
    echo "## Queue candidates"
    local i=0 queue_count=0
    while IFS= read -r item; do
      [[ -z "$item" ]] && continue
      i=$((i + 1))
      queue_count=$((queue_count + 1))
      if [[ "$i" -eq 1 ]]; then
        echo "- id=queue-next (recommended): $item"
      else
        echo "- id=queue-${i}: $item"
      fi
      if [[ "$i" -ge "$n" ]]; then
        break
      fi
    done < "$queue_tmp"
    if [[ "$i" -eq 0 ]]; then
      echo "- (none)"
    fi
    echo

    echo "## Suggested tasks"
    local suggest_target suggest_count
    suggest_target="$n"
    if [[ "$queue_count" -eq 0 && "$suggest_target" -lt 5 ]]; then
      suggest_target=5
    fi
    suggest_count=0
    while IFS=$'\t' read -r s_title s_goal s_scope s_acceptance; do
      [[ -z "$s_title" ]] && continue
      suggest_count=$((suggest_count + 1))
      echo "- id=suggested-${suggest_count}"
      echo "  - [ ] TODO Title: ${s_title}"
      echo "    Goal: ${s_goal}"
      echo "    Scope: ${s_scope}"
      echo "    Acceptance:"
      IFS=';' read -r -a accept_items <<< "$s_acceptance"
      local accept_printed=0
      for accept_item in "${accept_items[@]}"; do
        accept_item="$(echo "$accept_item" | sed -E 's/^ +| +$//g')"
        [[ -z "$accept_item" ]] && continue
        accept_printed=1
        echo "    - ${accept_item}"
      done
      if [[ "$accept_printed" -eq 0 ]]; then
        echo "    - [ ] make verify"
      fi
      if [[ "$suggest_count" -ge "$suggest_target" ]]; then
        break
      fi
    done < "$suggestions_tmp"
    if [[ "$suggest_count" -eq 0 ]]; then
      echo "- (none)"
    fi
    echo

    echo "## Recent decisions"
    i=0
    while IFS= read -r path; do
      [[ -z "$path" ]] && continue
      i=$((i + 1))
      echo "- $path"
      if [[ "$i" -ge "$n" ]]; then
        break
      fi
    done < "$decision_tmp"
    if [[ "$i" -eq 0 ]]; then
      echo "- (none)"
    fi
  } > "$proposal_file"

  echo "PROPOSAL_FILE: $proposal_file"
  echo "已生成候选清单（top ${n}）与 Suggested tasks。"
  echo "下一步：tools/task.sh --pick queue-next"
}

bootstrap_next_task() {
  local queue_file template_file output_dir
  queue_file="${TASK_BOOTSTRAP_QUEUE_FILE:-TASKS/QUEUE.md}"
  template_file="${TASK_BOOTSTRAP_TEMPLATE_FILE:-TASKS/_TEMPLATE.md}"
  output_dir="${TASK_BOOTSTRAP_OUTPUT_DIR:-TASKS}"

  if [[ ! -f "$queue_file" ]]; then
    echo "❌ QUEUE 文件不存在：$queue_file"
    exit 1
  fi
  if [[ ! -f "$template_file" ]]; then
    echo "❌ 模板文件不存在：$template_file"
    exit 1
  fi
  mkdir -p "$output_dir"

  local block title_line title goal scope_text acceptance_block
  block="$(awk '
    BEGIN { in_block = 0 }
    /^- \[ \] / {
      if (!in_block) {
        in_block = 1
        print
        next
      }
      if (in_block) {
        exit
      }
    }
    in_block { print }
  ' "$queue_file")"

  if [[ -z "$block" ]]; then
    echo "❌ QUEUE 中没有未完成项（- [ ]）"
    exit 1
  fi

  title_line="$(echo "$block" | awk 'NR==1 {print}')"
  title="$(echo "$title_line" | sed -E 's/^- \[ \][[:space:]]*TODO Title:[[:space:]]*//')"
  if [[ "$title" == "$title_line" ]]; then
    title="$(echo "$title_line" | sed -E 's/^- \[ \][[:space:]]*//')"
  fi
  title="$(echo "$title" | sed -E 's/[[:space:]]+$//')"
  if [[ -z "$title" ]]; then
    echo "❌ 无法从 QUEUE 提取 Title"
    exit 1
  fi

  goal="$(echo "$block" | awk -F'Goal:[[:space:]]*' '/^[[:space:]]*Goal:[[:space:]]*/ {print $2; exit}')"
  scope_text="$(echo "$block" | awk -F'Scope:[[:space:]]*' '/^[[:space:]]*Scope:[[:space:]]*/ {print $2; exit}')"
  acceptance_block="$(echo "$block" | awk '
    BEGIN { in_accept = 0 }
    /^[[:space:]]*Acceptance:[[:space:]]*$/ { in_accept = 1; next }
    in_accept && /^[[:space:]]*RUN_ID:/ { exit }
    in_accept && /^- \[[ x]\]/ { exit }
    in_accept {
      if ($0 ~ /^[[:space:]]*-[[:space:]]+/) {
        sub(/^[[:space:]]+/, "", $0)
        print $0
      }
    }
  ')"

  local slug run_date run_id task_file
  slug="$(slugify "$title")"
  run_date="$(date +%Y-%m-%d)"
  run_id="run-${run_date}-${slug}"

  task_file="${output_dir}/TASK-${slug}.md"
  if [[ -f "$task_file" ]]; then
    task_file="${output_dir}/TASK-${slug}-$(date +%H%M%S).md"
  fi

  {
    echo "# TASK: ${title}"
    echo
    echo "RUN_ID: ${run_id}"
    echo "OWNER: <you>"
    echo "PRIORITY: P1"
    echo
    echo "## Goal"
    if [[ -n "$goal" ]]; then
      echo "$goal"
    else
      echo "What outcome do we want? (1-3 lines)"
    fi
    echo
    
    echo "## Scope (Required)"
    if [[ -n "$scope_text" ]]; then
      # Normalize Scope into one-path-per-bullet.
      # Accepted input formats in QUEUE item:
      #   1) Backticked list: `tools/task.sh`, `tests/`, `TASKS/QUEUE.md`
      #   2) Single path without spaces: tests/
      local bt rest found path
      bt=$'\x60'
      rest="$scope_text"
      found=0

      if [[ "$rest" == *"$bt"*"$bt"* ]]; then
        # Extract all backticked segments.
        while [[ "$rest" == *"$bt"*"$bt"* ]]; do
          found=1
          rest="${rest#*${bt}}"
          path="${rest%%${bt}*}"
          echo "- ${bt}${path}${bt}"
          rest="${rest#*${bt}}"
        done 
      else
        # Backward-compat: allow a simple single path like tests/ (no spaces).
        if [[ "$rest" == *" "* ]]; then
          echo "❌ Invalid Scope in QUEUE item. Use backticked paths like: Scope: \`tools/task.sh\`, \`tests/\` (or a single no-space path like: Scope: tests/)" >&2
          exit 1
        fi
        found=1
        echo "- ${bt}${rest}${bt}"
      fi

      # Fail fast if we couldn't extract any scope path bullets.
      if [[ "$found" -eq 0 ]]; then
        echo "❌ Invalid Scope in QUEUE item: could not extract any scope paths." >&2
        exit 1
      fi
    else
      # No Scope provided in QUEUE item: provide a safe default scaffold.
      echo "- \`tools/task.sh\`"
      echo "- \`tests/\`"
      echo "- \`TASKS/QUEUE.md\`"
    fi
    echo
    echo "## Non-goals"
    echo "What we explicitly do NOT do."
    echo
    echo "## Acceptance"
    if [[ -n "$acceptance_block" ]]; then
      echo "$acceptance_block"
    else
      echo "- [ ] Command(s) pass: \`make verify\`"
      echo "- [ ] Evidence updated: \`reports/{RUN_ID}/summary.md\` and \`reports/{RUN_ID}/decision.md\`"
      echo "- [ ] Regression guardrail added/updated if applicable"
    fi
    echo
    echo "## Inputs"
    echo "- Links / files / references"
    echo "- If data is needed, specify allowed sample constraints (max rows, time window)"
    echo
    echo "## Steps (Optional)"
    echo "Suggested approach, if you have one."
    echo
    echo "## Reading policy"
    echo "Use \`tools/view.sh\` by default. If you need to read larger ranges, specify the"
    echo "exact line range and the reason."
    echo
    echo "## Risks / Rollback"
    echo "- Risks:"
    echo "- Rollback plan:"
  } > "$task_file"

  # mark the picked queue item as in-progress to avoid duplicate picks across sessions
  local queue_backup picked_ts evidence_cmd
  queue_backup="${queue_file}.bak.$$"
  cp "$queue_file" "$queue_backup"
  picked_ts="$(date +%Y-%m-%dT%H:%M:%S%z)"
  awk -v rid="$run_id" -v ts="$picked_ts" '
      BEGIN { done=0 }
      {
        if (!done && $0 ~ /^- \[ \] /) {
          done=1
          sub(/^- \[ \] /, "- [>] ")
          if ($0 !~ /Picked:/) {
            $0 = $0 "  Picked: " rid " " ts
          }
        }
        print
      }
    ' "$queue_file" > "${queue_file}.tmp" && mv "${queue_file}.tmp" "$queue_file"

  if [[ "${TASK_BOOTSTRAP_EVIDENCE:-1}" == "1" ]]; then
    if [[ -n "${TASK_BOOTSTRAP_EVIDENCE_CMD:-}" ]]; then
      evidence_cmd="${TASK_BOOTSTRAP_EVIDENCE_CMD}"
    else
      evidence_cmd="make evidence RUN_ID=\"$run_id\""
    fi
    if ! eval "$evidence_cmd"; then
      mv "$queue_backup" "$queue_file"
      echo "❌ Auto evidence failed; rolled back queue pick marker." >&2
      exit 1
    fi
  fi

  if [[ -f "$queue_backup" ]]; then
    rm -f "$queue_backup"
  fi

  echo "TASK_FILE: $task_file"
  echo "RUN_ID: $run_id"
  echo "EVIDENCE_PATH: reports/${run_id}/"
  echo "== 下一步清单 =="
  echo "1) tools/view.sh ${task_file}"
  echo "2) 按 Scope 做改动"
  echo "3) make verify"
  echo "4) 更新 reports/${run_id}/{summary,decision}"
  echo "5) RUN_ID=${run_id} tools/task.sh ${task_file}"
}

pick_task_interactive() {
  # 1. 先读取文件列表（无多余输出）
  mapfile -t files < <(find TASKS -maxdepth 2 -type f \( -name "*.md" -o -name "*.txt" \) \
    ! -path "*/.ipynb_checkpoints/*" \
    | sort)
  
  if [[ ${#files[@]} -eq 0 ]]; then
    echo "❌ TASKS/ 下没有 .md/.txt 文件"
    exit 1
  fi

  # 2. 提示语和选项列表输出到终端（stderr），不被变量捕获
  echo "请选择一个任务文件：" >&2
  local i=1
  for f in "${files[@]}"; do
    echo "$i) $f" >&2
    ((i++))
  done

  # 3. 手动读取输入，避免select的默认输出污染
  local selected=""
  while true; do
    echo -n "#? " >&2
    read -r choice
    # 校验输入是否为有效数字
    if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= ${#files[@]} )); then
      selected="${files[$((choice-1))]}"
      break
    fi
    echo "请输入有效编号。" >&2
  done

  # 4. 仅输出纯路径（stdout），被变量捕获
  echo "$selected"
}

task_file="${1:-}"

if [[ "$task_file" == "--plan" || "$task_file" == "plan" ]]; then
  task_plan_generate "${2:-20}"
  exit 0
fi

if [[ "$task_file" == "--pick" || "$task_file" == "pick" ]]; then
  pick_id="${2:-}"
  proposal_file="${TASK_PLAN_OUTPUT_FILE:-TASKS/TODO_PROPOSAL.md}"
  if [[ ! -f "$proposal_file" ]]; then
    echo "❌ 未找到 proposal：$proposal_file"
    echo "   请先运行：tools/task.sh --plan"
    exit 1
  fi
  if [[ "$pick_id" == "queue-next" ]]; then
    bootstrap_next_task
    exit 0
  fi
  echo "❌ Unsupported pick id: $pick_id"
  echo "   当前仅支持：queue-next"
  exit 1
fi

if [[ "$task_file" == "--next" || "$task_file" == "next" ]]; then
  bootstrap_next_task
  exit 0
fi

if [[ -z "$task_file" ]]; then
  task_file="$(pick_task_interactive)"
fi

task_file="$(echo "$task_file" | sed -E 's/^\s+|\s+$//g')" # 修复路径可能有前后空格

if [[ ! -f "$task_file" ]]; then
  echo "❌ 任务文件不存在：$task_file"
  exit 1
fi

# 提取任务标题：取第一行非空行；去掉常见 markdown 前缀
title="$(grep -m1 -E '\S' "$task_file" | sed -E 's/^\s*(#+|-|\*|\[ \]|\[x\])\s*//g' | sed -E 's/^\s+|\s+$//g')"
if [[ -z "$title" ]]; then
  title="$(basename "$task_file")"
fi

msg="task: ${title}"
if [[ -n "${RUN_ID:-}" ]]; then
  msg="${RUN_ID}: ${msg}"
fi

echo "任务文件：$task_file"
echo "生成提交信息：$msg"
echo

# 给个小提示：避免误提 ship 本体
if git status --porcelain | grep -q "tools/ship.sh"; then
  echo "⚠️  你当前工作区包含 tools/ship.sh 改动，建议先：git restore tools/ship.sh"
  echo "    否则 ship 的保险丝会拦截（除非你明确 SHIP_ALLOW_SELF=1）"
  echo
fi

# 提交和创建 PR
SHIP_TASK_FILE="$task_file" SHIP_TASK_TITLE="$title" tools/ship.sh "$msg"
