#!/usr/bin/env bash
set -euo pipefail

# tools/ship.sh v1.0.3
# ------------------------------------------------------------
# 目标：在开启 main 分支保护（必须 PR + 必须 CI check）下，
#      一键把“当前工作区改动”发成 PR，并在 CI 通过后自动合并。
#
# v1.0.1: 修复 stash_ref 末尾冒号导致 stash pop 失败
# v1.0.2: 刚建 PR 会暂时 no checks reported -> 等待 checks 出现再 watch
# v1.0.3:
#   - PR 描述自动生成（中文，包含 diff 摘要/文件列表/验证方式/合并策略）
#   - auto-merge 已合并时不再重复 merge（避免 already merged 提示）
# ------------------------------------------------------------

MSG="${1:-}"
if [[ -z "$MSG" ]]; then
  echo "用法：tools/ship.sh \"一句话说明改动\""
  exit 1
fi

# 0) 确认 gh 已登录
gh auth status -h github.com >/dev/null

# 1) 确保在仓库根目录
git rev-parse --is-inside-work-tree >/dev/null

# 2) 记录当前分支
orig_branch="$(git rev-parse --abbrev-ref HEAD)"

# 3) 如有改动，先 stash（否则 pull --rebase 会失败）
STASH_NAME=""
if ! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git ls-files --others --exclude-standard)" ]]; then
  STASH_NAME="ship-wip-$(date +%Y%m%d-%H%M%S)"
  echo "Detected local changes. Stashing as: $STASH_NAME"
  git stash push -u -m "$STASH_NAME" >/dev/null
fi

# 4) 生成分支名
ts="$(date +%Y%m%d-%H%M%S)"
slug="$(echo "$MSG" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g' | sed -E 's/^-+|-+$//g' | cut -c1-40)"
branch="chore/${slug:-update}-${ts}"

# 5) 同步 main（保证从最新 main 切分支）
git fetch origin
git checkout main >/dev/null 2>&1 || git checkout -b main origin/main
git pull --rebase origin main

# 6) 建分支
git checkout -b "$branch"

# 7) 把 stash 恢复到新分支上（如果有）
if [[ -n "$STASH_NAME" ]]; then
  echo "Restoring stashed changes onto $branch ..."

  stash_ref="$(git stash list \
    | awk -v name="$STASH_NAME" '$0 ~ name {print $1}' \
    | head -n1 \
    | sed 's/:$//' \
    || true)"

  if [[ -z "$stash_ref" ]]; then
    echo "ERROR: Could not find stash named $STASH_NAME"
    echo "Run: git stash list"
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

（或者你也可以手动 commit/push/PR）

EOF2
    exit 1
  fi
fi

# 8) 提交
git add -A
if git diff --cached --quiet; then
  echo "No changes staged. Nothing to commit."
  echo "You are on branch: $branch"
  exit 0
fi

git commit -m "$MSG"
git push -u origin "$branch"

# 9) 自动生成中文 PR 描述（v1.0.3）
stat="$(git diff --stat origin/main...HEAD || true)"
files="$(git diff --name-only origin/main...HEAD || true)"

# 截断，避免 body 太长
stat_short="$(echo "$stat" | head -n 60)"
files_short="$(echo "$files" | head -n 120)"

PR_BODY="$(cat <<EOF3
## 变更概述
- 由 \`tools/ship.sh v1.0.3\` 自动生成
- 合并策略：Squash
- 说明：CI 通过后自动合并（如仓库允许 Auto-merge）

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

# 10) 创建 PR（标题用 MSG）
pr_url="$(gh pr create --base main --head "$branch" --title "$MSG" --body "$PR_BODY")"
echo "PR: $pr_url"

# 11) 开启 auto-merge（CI 绿自动合并）+ 合并后删远端分支
# 若仓库未允许 auto-merge，这里会失败；后面仍会等待 checks，再尝试手动 merge
gh pr merge --auto --squash --delete-branch "$pr_url" || true

# 12) v1.0.2: 有时刚建 PR 会暂时 "no checks reported"，先等待 checks 出现再 watch
for i in {1..30}; do
  if gh pr checks "$pr_url" >/dev/null 2>&1; then
    break
  fi
  echo "Waiting for checks to appear... ($i/30)"
  sleep 2
done

gh pr checks --watch "$pr_url"

# 13) v1.0.3: 如果 auto-merge 已经合并，就不再重复 merge
state="$(gh pr view "$pr_url" --json state -q .state)"
if [[ "$state" != "MERGED" ]]; then
  gh pr merge --squash --delete-branch "$pr_url" || true
fi

# 14) 回 main 同步
git checkout main
git pull --rebase origin main

# 15) 清理本地分支（如果已合并）
git branch -D "$branch" >/dev/null 2>&1 || true

echo "Done. (started from: $orig_branch)"