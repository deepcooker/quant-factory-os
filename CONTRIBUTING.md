# CONTRIBUTING（贡献指南）

## 1）硬规则：禁止直接 push main
`main` 分支受保护，任何改动必须通过 Pull Request（PR）进入 `main`。

- 不允许直接 `git push origin main`
- 不允许绕过门禁（bypass）

---

## 2）唯一入口：用 tools/ship.sh 发货（人 + Codex + API 都一样）
你改完任何文件后，只执行：

```bash
tools/ship.sh "一句话说明改动"
```

脚本会自动完成：

* （如有需要）stash 本地改动
* 更新 `main` 到最新
* 新建分支
* 自动 `git add / commit / push`
* 自动创建 PR
* 等 CI 绿灯（required checks）
* 自动合并（squash）并删除分支
* 回到 `main` 并同步最新

---

## 3）标题建议（可选，但推荐）

为了让提交历史清晰，建议在标题前加前缀：

* `docs:` 文档
* `chore:` 工具/杂项
* `fix:` 修复
* `feat:` 新功能

示例：

```bash
tools/ship.sh "fix: 修复 ws 重连边界情况"
tools/ship.sh "docs: 补充贡献指南"
```