#!/usr/bin/env bash
set -euo pipefail

# 用法：
#   tools/ship.sh "commit message"
# 例子：
#   tools/ship.sh "docs: add onboarding notes"

MSG="${1:-}"
if [[ -z "$MSG" ]]; then
  echo "Usage: tools/ship.sh \"commit message\""
  exit 1
fi

# 0) 确认 gh 已登录
gh auth status -h github.com >/dev/null

# 1) 确保在仓库根目录
git rev-parse --is-inside-work-tree >/dev/null

# 2) 生成分支名
ts="$(date +%Y%m%d-%H%M%S)"
slug="$(echo "$MSG" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-+|-+$//g' | cut -c1-40)"
branch="chore/${slug:-update}-${ts}"

# 3) 同步 main
git fetch origin
git checkout main
git pull --rebase origin main

# 4) 建分支 + 提交
git checkout -b "$branch"
git add -A

if git diff --cached --quiet; then
  echo "No changes staged. Nothing to commit."
  exit 0
fi

git commit -m "$MSG"
git push -u origin "$branch"

# 5) 创建 PR（--fill 会用 commit message 自动填标题/描述）
pr_url="$(gh pr create --base main --head "$branch" --fill)"
echo "PR: $pr_url"

# 6) 开启 auto-merge（CI 绿自动合并）+ 合并后删分支
# 需要你仓库 Settings 已开启 Allow auto-merge
gh pr merge --auto --squash --delete-branch "$pr_url" || true

# 7) 盯 CI（直到通过/失败）
gh pr checks --watch "$pr_url"

# 8) 如果 auto-merge 因设置原因没生效，尝试手动 merge（满足门禁才会成功）
gh pr merge --squash --delete-branch "$pr_url" || true

# 9) 回 main 同步
git checkout main
git pull --rebase origin main

echo "Done."
