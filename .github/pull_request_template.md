## 任务文件路径
\`\`\`
${task_file_path}
\`\`\`

## 变更概述
- 任务：${task_title}
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
