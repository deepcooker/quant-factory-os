# TASK: Codex CI 自动修复与宪法化入职模板

RUN_ID: run-2026-02-27-codex-ci-autofix-and-onboarding-constitution
OWNER: <you>
PRIORITY: P1

## Goal
为仓库新增可直接启用的 Codex 自动化模板：CI 失败自动修复工作流，以及一次 session 的宪法化入职/培训文档模板，降低大项目协作漂移。

## Scope (Required)
- `AGENTS.md`
- `tools/`
- `.github/workflows/`
- `docs/`
- `chatlogs/`
- `tests/`
- `TASKS/`
- `reports/{RUN_ID}/`

## Non-goals
- 不修改业务代码与策略逻辑。
- 不接入真实生产密钥或真实生产数据。

## Acceptance
- 新增可审阅的 GitHub Actions 模板：review + autofix 两条工作流（默认安全开关关闭或受条件限制）。
- 新增宪法化入职模板，覆盖：环境确认、必读清单、复述验收、上岗 gate。
- `make verify` 通过，且本 RUN_ID evidence 三件套完整。

## Inputs
- `chatlogs/PROJECT_GUIDE.md`
- OpenAI Codex 官方文档（slash-commands / noninteractive / github-action / agents-md / config-reference）

## Steps (Optional)
1) 生成 evidence 骨架。
2) 以最小 diff 添加 workflow 与文档模板。
3) 运行 verify。
4) 回填 reports 决策与总结。

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: CI 权限配置不当会导致自动化失效或误触发。
- Rollback plan: 回滚新增 workflow 与模板文档，恢复到上一提交。
