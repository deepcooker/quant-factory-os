#!/usr/bin/env bash
set -euo pipefail

#   tools/task.sh v0.6 终极修复版
# - 彻底解决交互选择路径污染（分离stdout/stderr）
# - 忽略 .ipynb_checkpoints 文件夹中的文件
# - 加固路径清洗逻辑

repo_root="$(git rev-parse --show-toplevel)"
cd "$repo_root"

if [[ ! -d "TASKS" ]]; then
  echo "❌ 找不到 TASKS/ 目录（请先创建或同步）" >&2
  exit 1
fi

pick_task_interactive() {
  # 1. 读取文件列表（无任何输出）
  mapfile -t files < <(find TASKS -maxdepth 2 -type f \( -name "*.md" -o -name "*.txt" \) \
    ! -path "*/.ipynb_checkpoints/*" \
    | sort)
  
  if [[ ${#files[@]} -eq 0 ]]; then
    echo "❌ TASKS/ 下没有 .md/.txt 文件" >&2
    exit 1
  fi

  # 2. 提示语输出到stderr（只显示，不被捕获）
  echo "请选择一个任务文件：" >&2
  
  # 3. 循环等待有效输入，避免select的默认输出污染
  local selected=""
  local i=1
  # 先打印选项列表（输出到stderr）
  for f in "${files[@]}"; do
    echo "$i) $f" >&2
    ((i++))
  done
  # 读取用户输入
  while true; do
    echo -n "#? " >&2
    read -r choice
    # 校验输入是否为数字、且在有效范围
    if [[ "$choice" =~ ^[0-9]+$ ]] && (( choice >= 1 && choice <= ${#files[@]} )); then
      selected="${files[$((choice-1))]}"
      break
    fi
    echo "请输入有效编号（1-${#files[@]}）。" >&2
  done

  # 4. 仅输出选中的纯路径到stdout（被变量捕获）
  echo "$selected"
}

task_file="${1:-}"
if [[ -z "$task_file" ]]; then
  # 调用交互函数，仅捕获纯路径
  task_file="$(pick_task_interactive)"
fi

# 加固路径清洗：去掉所有空格/不可见字符
task_file="$(echo "$task_file" | sed -E 's/^[[:space:]]+|[[:space:]]+$//g' | tr -d '\r\n')"

if [[ ! -f "$task_file" ]]; then
  echo "❌ 任务文件不存在：$task_file" >&2
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

# 触发发货（PR 模板会自动出现；PR body 由 ship 自动生成）
tools/ship.sh "$msg"