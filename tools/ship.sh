#!/usr/bin/env bash
set -euo pipefail

# tools/ship.sh v1.0.3
# ------------------------------------------------------------
# v1.0.1: 修复 stash_ref 末尾冒号导致 stash pop 失败
# v1.0.2: 刚建 PR 会暂时 no checks reported -> 等待 checks 出现再 watch
# v1.0.3:
#   - PR 描述自动生成（中文，包含 diff 摘要/文件列表/验证方式/合并策略）
#   - auto-merge 已合并时不再重复 merge（减少噪音）
#   - 合并后尽量清理本地/远端分支（依赖 auto-merge 配置）
# ------------------------------------------------------------

MSG="${1:-}"
if [[ -z "$MSG" ]]; then
  echo "用法：tools/ship.sh \"一句话说明改动\""
  exit 1
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

git add -A
if git diff --cached --quiet; then
  echo "No changes staged. Nothing to commit."
  echo "You are on branch: $branch"
  exit 0
fi

git commit -m "$MSG"
git push -u origin "$branch"

# --- 中文 PR 描述自动生成 ---
stat="$(git diff --stat origin/main...HEAD || true)"
files="$(git diff --name-only origin/main...HEAD || true)"
stat_short="$(echo "$stat" | head -n 60)"
files_short="$(echo "$files" | head -n 120)"

PR_BODY="$(cat <<EOF3
## 变更概述
- 由 \`tools/ship.sh v1.0.3\` 自动生成
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

pr_url="$(gh pr create --base main --head "$branch" --title "$MSG" --body "$PR_BODY")"
echo "PR: $pr_url"

gh pr merge --auto --squash --delete-branch "$pr_url" || true

# 等待 checks 出现再 watch（避免 no checks reported）
for i in {1..30}; do
  if gh pr checks "$pr_url" >/dev/null 2>&1; then
    break
  fi
  echo "Waiting for checks to appear... ($i/30)"
  sleep 2
done
gh pr checks --watch "$pr_url"

# 如果 auto-merge 已经合并，就不再重复 merge
state="$(gh pr view "$pr_url" --json state -q .state)"
if [[ "$state" != "MERGED" ]]; then
  gh pr merge --squash --delete-branch "$pr_url" || true
fi

git checkout main
git pull --rebase origin main

# 尽量清理本地分支
git branch -D "$branch" >/dev/null 2>&1 || true

echo "Done. (started from: $orig_branch)"