#!/usr/bin/env bash
set -euo pipefail

# tools/ship.sh v1.0.1
# ------------------------------------------------------------
# 目标：在开启 main 分支保护（必须 PR + 必须 CI check）下，
#      一键把“当前工作区改动”发成 PR，并在 CI 通过后自动合并。
#
# v1.0.1 变更：
# - 修复：stash_ref 取到的是 "stash@{0}:"（末尾带冒号），导致 git stash pop 失败
# - 增强：stash pop 使用 --index（如果你本来有 staged 内容也能尽量还原）
# ------------------------------------------------------------

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

  # stash@{0}: 末尾通常会带冒号，这里要去掉
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
    cat <<EOF

⚠️ stash pop 未能自动应用（可能有冲突）。
请你手动处理后再继续：

  1) git status
  2) 解决冲突后：git add -A
  3) 然后再运行一次：
     tools/ship.sh "$MSG"

（或者你也可以手动 commit/push/PR）

EOF
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

# 9) 创建 PR（--fill 会用 commit message 自动填标题/描述）
pr_url="$(gh pr create --base main --head "$branch" --fill)"
echo "PR: $pr_url"

# 10) 开启 auto-merge（CI 绿自动合并）+ 合并后删远端分支
# 如果仓库没开 Auto-merge，会报 enablePullRequestAutoMerge；这里允许继续走后面的手动 merge
gh pr merge --auto --squash --delete-branch "$pr_url" || true

# 11) 盯 CI（直到通过/失败）
# v1.0.2: 有时刚建 PR 会暂时 "no checks reported"，先等待 checks 出现再 watch
for i in {1..30}; do
  if gh pr checks "$pr_url" >/dev/null 2>&1; then
    break
  fi
  echo "Waiting for checks to appear... ($i/30)"
  sleep 2
done

gh pr checks --watch "$pr_url"


# 12) 如果 auto-merge 没生效，尝试手动 merge（满足门禁才会成功）
gh pr merge --squash --delete-branch "$pr_url" || true

# 13) 回 main 同步
git checkout main
git pull --rebase origin main

# 14) 清理本地分支（如果已合并）
git branch -D "$branch" >/dev/null 2>&1 || true

echo "Done. (started from: $orig_branch)"
