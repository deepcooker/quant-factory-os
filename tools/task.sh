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
      echo "- \`${scope_text}\`"
    else
      echo "- List allowed paths for this task using bullets and backticks, for example:"
      echo "  - \`tools/ship.sh\`"
      echo "  - \`tests/\`"
    fi
    echo "- \`tools/ship.sh\` uses this section as the source of truth for scope gate checks."
    echo
    echo "## Non-goals"
    echo "What we explicitly do NOT do."
    echo
    echo "## Acceptance"
    if [[ -n "$acceptance_block" ]]; then
      echo "$acceptance_block"
    else
      echo "- [ ] Command(s) pass: \`make verify\`"
      echo "- [ ] Evidence updated: \`reports/<RUN_ID>/summary.md\` and \`reports/<RUN_ID>/decision.md\`"
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

  if [[ "${TASK_BOOTSTRAP_EVIDENCE:-0}" == "1" ]]; then
    make evidence RUN_ID="$run_id"
  fi

  echo "TASK_FILE: $task_file"
  echo "RUN_ID: $run_id"
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
