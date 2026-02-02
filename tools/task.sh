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

echo "任务文件：$task_file"
echo "生成提交信息：$msg"
echo

# 给个小提示：避免误提 ship 本体
if git status --porcelain | grep -q "tools/ship.sh"; then
  echo "⚠️  你当前工作区包含 tools/ship.sh 改动，建议先：git restore tools/ship.sh"
  echo "    否则 ship 的保险丝会拦截（除非你明确 SHIP_ALLOW_SELF=1）"
  echo
fi

# 自动生成 PR 描述，包含任务路径
PR_BODY=$(cat <<EOF2
## 任务文件路径
\`\`\`
$task_file
\`\`\`

## 变更概述
- 任务：${title}
- 合并策略：Squash
- 说明：CI 通过后自动合并（Auto-merge）

## 变更范围（git diff --stat）
\`\`\`
$(git diff --stat origin/main...HEAD || true)
\`\`\`

## 涉及文件
\`\`\`
$(git diff --name-only origin/main...HEAD || true)
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
EOF2
)

# 提交和创建 PR
tools/ship.sh "$msg"