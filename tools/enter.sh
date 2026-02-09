#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
cwd="$(pwd)"
if [[ -z "$repo_root" ]]; then
  echo "❌ 不在 git 仓库内"
  echo "   修复：cd 到仓库根目录后再运行"
  exit 1
fi

if [[ "$cwd" != "$repo_root" ]]; then
  echo "❌ 请在仓库根目录运行 tools/enter.sh"
  echo "   修复：cd \"$repo_root\""
  exit 1
fi

branch="$(git branch --show-current)"
echo "branch: ${branch}"

if ! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git ls-files --others --exclude-standard)" ]]; then
  echo "❌ 工作区不干净（有未提交改动）"
  echo "   修复：先运行 tools/task.sh 走 ship/stash，或手工处理未提交改动"
  exit 1
fi

echo "✅ 工作区干净，开始同步"
if ! git pull --rebase; then
  echo "❌ git pull --rebase 失败"
  echo "   修复：解决冲突后再重试"
  exit 1
fi

echo "== running doctor =="
if ! bash tools/doctor.sh; then
  echo "❌ doctor 失败，请按提示修复"
  exit 1
fi

echo
echo "== 下一步建议 =="
if [[ -f "TASKS/QUEUE.md" ]]; then
  echo "运行：tools/task.sh 并选择队列任务"
else
  echo "创建新任务：在 TASKS/ 下新增 TASK 文件"
fi
