# Summary

RUN_ID: `run-2026-03-11-vnext-release-baseline`

## rebuild repo-local skills from latest orchestrator design
- 本轮按根目录的最新实验设计，重建了 repo-local skills。
- 已删除旧 skill 文件内容与旧骨架语义：
  - `baseline-learn`
  - `baseline-refresh`
  - `fork-identity`
  - `role-worker`
  - `root-python-smoke`
  - `session-coach`
  - `task-referee`
- 新的正式 repo-local skill 集现在是：
  - [learn-baseline](/root/quant-factory-os/.agents/skills/learn-baseline/SKILL.md)
  - [project-coach](/root/quant-factory-os/.agents/skills/project-coach/SKILL.md)
  - [run-manager](/root/quant-factory-os/.agents/skills/run-manager/SKILL.md)
  - [demand-critic](/root/quant-factory-os/.agents/skills/demand-critic/SKILL.md)
  - [solution-designer](/root/quant-factory-os/.agents/skills/solution-designer/SKILL.md)
  - [risk-reviewer](/root/quant-factory-os/.agents/skills/risk-reviewer/SKILL.md)
  - [doc-evidence-worker](/root/quant-factory-os/.agents/skills/doc-evidence-worker/SKILL.md)
  - [code-evidence-worker](/root/quant-factory-os/.agents/skills/code-evidence-worker/SKILL.md)
  - [runtime-evidence-worker](/root/quant-factory-os/.agents/skills/runtime-evidence-worker/SKILL.md)
  - [contradiction-checker](/root/quant-factory-os/.agents/skills/contradiction-checker/SKILL.md)
  - [dev-worker](/root/quant-factory-os/.agents/skills/dev-worker/SKILL.md)
  - [test-worker](/root/quant-factory-os/.agents/skills/test-worker/SKILL.md)
  - [arch-reviewer](/root/quant-factory-os/.agents/skills/arch-reviewer/SKILL.md)
- 根目录 [skills/](/root/quant-factory-os/skills) 已同步生成可视化镜像，便于页面直接查看。
- 这轮只建骨架，不深写协议内容；每个 skill 当前都只有：
  - 合法 `SKILL.md`
  - 合法 `agents/openai.yaml`
  - 最小中文展示层和用途说明
- 真实验证已完成：
  - 13 个 skill 全部通过官方 `quick_validate.py`
  - `docs/FILE_INDEX.md` 已把旧 skill 索引切换到新的 13 个名字
- 当前结论：
  - 新 skill 集已经与根目录实验设计对齐
  - 但它们仍是实验性骨架，后续要按 owner 的分步计划逐个补方法论、脚本和 appserver 交互方式
- step1 继续核对后，已经确认：
  - [project-coach](/root/quant-factory-os/skills/project-coach/SKILL.md)
  - [run-manager](/root/quant-factory-os/skills/run-manager/SKILL.md)
  - [doc-evidence-worker](/root/quant-factory-os/skills/doc-evidence-worker/SKILL.md)
  三份正文与 [skill_step1.md](/root/quant-factory-os/skill_step1.md) 的语义一致。
- 这轮没有改这三份正文方法论，只把它们从镜像目录同步写进了正式 repo-local 目录：
  - [project-coach](/root/quant-factory-os/.agents/skills/project-coach/SKILL.md)
  - [run-manager](/root/quant-factory-os/.agents/skills/run-manager/SKILL.md)
  - [doc-evidence-worker](/root/quant-factory-os/.agents/skills/doc-evidence-worker/SKILL.md)
- 两边 `agents/openai.yaml` 继续保持一致，镜像和正式 skill 现在对齐。
- step2 继续核对后，已经确认：
  - [code-evidence-worker](/root/quant-factory-os/skills/code-evidence-worker/SKILL.md)
  的正文语义与 [skill_step2.md](/root/quant-factory-os/skill_step2.md) 一致。
- 本轮只做了最小修正：
  - 修掉 `code-evidence-worker` 里多余的 markdown code fence 结束标记
  - 把根目录镜像版同步写入正式 repo-local 目录：
    - [code-evidence-worker](/root/quant-factory-os/.agents/skills/code-evidence-worker/SKILL.md)
  - 同时把两边的 `agents/openai.yaml` 对齐到更贴合正文语义的描述
- 配置核对结果：
  - 根目录 [project_config.json](/root/quant-factory-os/project_config.json) 与 step2 的字段设计一致
  - `state/registry.json` 目前仓库里还不存在，因此这一步只确认了配置设计，不认定 registry 已落地
- step3 重新核对后，已经确认：
  - [runtime-evidence-worker](/root/quant-factory-os/skills/runtime-evidence-worker/SKILL.md)
  - [demand-critic](/root/quant-factory-os/skills/demand-critic/SKILL.md)
  - [solution-designer](/root/quant-factory-os/skills/solution-designer/SKILL.md)
  的正文语义与 [skill_step3.md](/root/quant-factory-os/skill_step3.md) 一致。
- 这轮只对这 3 份做了最小格式修正：
  - 修掉多余的 markdown fence 结束标记
  - 统一列表格式
- 并已同步到正式 repo-local 目录：
  - [runtime-evidence-worker](/root/quant-factory-os/.agents/skills/runtime-evidence-worker/SKILL.md)
  - [demand-critic](/root/quant-factory-os/.agents/skills/demand-critic/SKILL.md)
  - [solution-designer](/root/quant-factory-os/.agents/skills/solution-designer/SKILL.md)
- 同时两边 yaml 已对齐成更贴合正文的展示说明。
- `risk-reviewer` 重新贴正后，这轮也已完成：
  - [risk-reviewer](/root/quant-factory-os/skills/risk-reviewer/SKILL.md)
  - [risk-reviewer](/root/quant-factory-os/.agents/skills/risk-reviewer/SKILL.md)
- 这份也只做了最小格式修正，没有改方法论正文。
- 两边 yaml 也已同步成与正文更一致的说明。
- step4 继续核对后，已经确认：
  - [contradiction-checker](/root/quant-factory-os/skills/contradiction-checker/SKILL.md)
  的正文语义与 [skill_step4.md](/root/quant-factory-os/skill_step4.md) 中对应段落一致。
- 这轮已把它同步到正式 repo-local 目录：
  - [contradiction-checker](/root/quant-factory-os/.agents/skills/contradiction-checker/SKILL.md)
- 镜像与正式版的 `SKILL.md` / `agents/openai.yaml` 已重新对齐，并再次通过官方 validator。
- [schemas](/root/quant-factory-os/schemas) 当前承载的是 role result schema 模板，不是运行产物；其中 `.ipynb_checkpoints` 属于噪音目录。

## bootstrap appserverskillclient with root-python-smoke
- 本轮新增了实验性客户端：
  - [appserverskillclient.py](/root/quant-factory-os/tools/appserverskillclient.py)
- 它当前只做最小一件事：
  - 从 Python 里显式拼出 `Use $skill-name ...`
  - 再通过 `codex exec` 调 repo-local skill
- 这轮刻意不改：
  - [appserverclient.py](/root/quant-factory-os/tools/appserverclient.py)
- 第一次试点绑定的是：
  - [root-python-smoke](/root/quant-factory-os/.agents/skills/root-python-smoke/SKILL.md)
- 真实验证已经通过：
  - `python3 -m py_compile tools/appserverskillclient.py`
  - `python3 tools/appserverskillclient.py --skill root-python-smoke --prompt 'run the root smoke test'`
- 真实返回结果显示：
  - 显式 skill prompt 为 `Use $root-python-smoke run the root smoke test`
  - skill 被成功触发
  - `skill_test_one.py` 输出 `1`
  - `skill_test_two.py` 输出 `2`
  - smoke test passed
- 这证明了当前最小链路已经成立：
  - `Python client -> codex exec -> repo-local skill -> shell actions -> final answer`
- 同时本轮最小文档已补：
  - [docs/WORKFLOW.md](/root/quant-factory-os/docs/WORKFLOW.md)
  - [docs/FILE_INDEX.md](/root/quant-factory-os/docs/FILE_INDEX.md)
  现在都明确把 `appserverskillclient` 标成“实验性 skill 调用入口”，不是 formal mainline 的 session runtime。

## localize six core protocol skills to Chinese
- 本轮把 6 个协议层 skill 的展示层和正文做了最小中文化：
  - [baseline-learn](/root/quant-factory-os/.agents/skills/baseline-learn/SKILL.md)
  - [fork-identity](/root/quant-factory-os/.agents/skills/fork-identity/SKILL.md)
  - [run-manager](/root/quant-factory-os/.agents/skills/run-manager/SKILL.md)
  - [role-worker](/root/quant-factory-os/.agents/skills/role-worker/SKILL.md)
  - [task-referee](/root/quant-factory-os/.agents/skills/task-referee/SKILL.md)
  - [baseline-refresh](/root/quant-factory-os/.agents/skills/baseline-refresh/SKILL.md)
- 中文化范围：
  - `agents/openai.yaml` 的 `display_name / short_description / default_prompt`
  - `SKILL.md` 正文的最小说明层
- 保持不变：
  - 内部 `name`
  - 目录名
- 这样做的目的是：
  - 让 owner 在 `/skills` 里看得懂
  - 同时保持 `$baseline-learn` 这类内部触发名稳定
- 六个 skill 在中文化后继续全部通过官方 validator。

## bootstrap six core protocol skills
- 本轮按 owner 刚刚确认的主线分层，在 `.agents/skills/` 下建立了 6 个正式 repo-local skill 骨架：
  - [baseline-learn](/root/quant-factory-os/.agents/skills/baseline-learn/SKILL.md)
  - [fork-identity](/root/quant-factory-os/.agents/skills/fork-identity/SKILL.md)
  - [run-manager](/root/quant-factory-os/.agents/skills/run-manager/SKILL.md)
  - [role-worker](/root/quant-factory-os/.agents/skills/role-worker/SKILL.md)
  - [task-referee](/root/quant-factory-os/.agents/skills/task-referee/SKILL.md)
  - [baseline-refresh](/root/quant-factory-os/.agents/skills/baseline-refresh/SKILL.md)
- 这轮只做骨架，不先写重逻辑。
- 每个 skill 当前都具备：
  - `SKILL.md`
  - `agents/openai.yaml`
  - 最小合法 `name/description` frontmatter
- 已完成的真实验证：
  - 6 个 skill 逐个通过官方 `quick_validate.py`
- 同时 [FILE_INDEX.md](/root/quant-factory-os/docs/FILE_INDEX.md) 已补最小索引，方便你直接点开检查。

## clarify root-python-smoke appserver skill invocation
- 本轮没有改 `root-python-smoke` 的行为，只改了它的说明层。
- 新增了 `Invocation Model` 段，明确：
  - `root-python-smoke` 是被 Codex/appserver 调起的 skill
  - 不是直接执行的 shell 命令
  - `Use $root-python-smoke ...` 才是正确入口
- shell 命令现在被清楚定义成：
  - skill 触发后模型应执行的动作
  - 而不是 skill 自己的外部使用方式
- 改完后 validator 继续通过：
  - `python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/root-python-smoke`

## standardize repo-local session-coach skill
- 本轮先对比了 3 个系统 skills 的正式产物：
  - `openai-docs`
  - `skill-creator`
  - `skill-installer`
- 对比结果一致：
  - 都有 `SKILL.md`
  - 都使用 `name/description` frontmatter
  - 都推荐配 `agents/openai.yaml`
- 因此已把 `session-coach` 按官方 repo-local skill 方式正式落位到：
  - [session-coach](/root/quant-factory-os/.agents/skills/session-coach/SKILL.md)
- 当前正式 session-coach skill 已具备：
  - `name: session-coach`
  - `description: ...`
  - [agents/openai.yaml](/root/quant-factory-os/.agents/skills/session-coach/agents/openai.yaml)
- 真实验证已通过：
  - `python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/session-coach`
  - `codex exec -C /root/quant-factory-os "Use $session-coach ..."`
- `codex exec` 日志已明确出现：
  - `Using session-coach for a baseline identity confirmation step`
- 这说明：
  - `session-coach` 现在已经不是仓库里的随手草稿
  - 而是符合官方 repo-local 规则的可发现 skill
- 旧的：
  - [skills/session-coach/SKILL.md](/root/quant-factory-os/skills/session-coach/SKILL.md)
  目前只保留为迁移前草稿参考，不再是正式落位。

## remove obsolete init-project fixtures
- 本轮已删除旧的 `fixtures/` 目录：
  - `fixtures/init_project_fixture`
  - `fixtures/init_project_real_material_fixture`
- 这两套目录是旧的 `init-project` 测试夹具，不属于当前 formal mainline，也不属于 repo-local skills。
- 当前正式主线和活代码已确认不再依赖它们；这轮检查到的残留引用只出现在：
  - 历史 `reports/` evidence
  - `project_all_files.txt`
- 因此这次删除属于主线去噪，不影响当前 baseline / fork-current / session / git 主线。

## repo-local skills smoke test hardening
- 本轮先不把 `session-coach` 直接当成正式 skill 推出去，而是按官方 skill 规范做了一次最小 smoke test。
- 新增了官方 repo-local 位置下的最小 skill：
  - [root-python-smoke](/root/quant-factory-os/.agents/skills/root-python-smoke/SKILL.md)
- 新增根目录 smoke 文件：
  - [skill_test_one.py](/root/quant-factory-os/skill_test_one.py)
  - [skill_test_two.py](/root/quant-factory-os/skill_test_two.py)
- 已完成三层验证：
  - `python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/root-python-smoke`
  - `python3 skill_test_one.py && python3 skill_test_two.py`
  - `codex exec -C /root/quant-factory-os "Use $root-python-smoke ..."`
- 最关键的真实结论：
  - repo-local skill 的正式落位是 `.agents/skills/`
  - 不是普通 repo-root `skills/` 目录
  - `codex exec` 日志已明确出现 `Using root-python-smoke for this turn`
- 本轮也顺手把 [FILE_INDEX.md](/root/quant-factory-os/docs/FILE_INDEX.md) 改成了这套正式口径：
  - `.agents/skills/` 是官方 repo-local skill 入口
  - `skills/session-coach/SKILL.md` 当前只是早期草稿，不是正式落位
- 当前 `fixtures/` 目录没有参与这轮 smoke test；它是旧的 `init-project` fixture 资产，不是 skills 目录。

## session-coach protocol / skill bootstrap
- 本轮新增了一个极简的个人多窗口协作协议：
  - [docs/SESSION_COACH_PROTOCOL.md](/root/quant-factory-os/docs/SESSION_COACH_PROTOCOL.md)
- 它只服务于当前最真实的使用场景：
  - 一个 `baseline` 窗口
  - 一个 `fork-run` 窗口
  - 一个幕后 `coach` 窗口
- 协议内容只固定四类动作：
  - 先确认身份
  - 再给下一条问题或命令
  - 再判断是否 `pass/retry`
  - 最后给下一跳
- 本轮同时新增了一个仓库内 skill 模板：
  - [skills/session-coach/SKILL.md](/root/quant-factory-os/skills/session-coach/SKILL.md)
- 当前决定是不做自动多窗口控制器，也不假装 skill 可以直接控制其他终端；先把“提问 / 验收 / 下一跳”的协议固定下来，再决定是否把这份模板安装到 `~/.codex/skills/`。
- 为避免文件落地后仍挂在旧 cleanup task，本轮已把：
  - `tools/project_config.json -> runtime_state.current_task_*`
  - `TASKS/QUEUE.json`
  切到新的：
  - `task-session-coach-skill-bootstrap`
- 相关最小入口也已补到：
  - [docs/WORKFLOW.md](/root/quant-factory-os/docs/WORKFLOW.md)
  - [docs/FILE_INDEX.md](/root/quant-factory-os/docs/FILE_INDEX.md)

## learnbaseline / init-project effort override and sandbox cleanup
- foundation 与 `/root/a9quant-strategy` 的 `tools/appserverclient.py` 当前已保持完全一致。
- 本轮给两条主线都补了最小参数面：
  - `python3 tools/appserverclient.py --learnbaseline [-new] -e <low|medium|high|xhigh>`
  - `python3 tools/appserverclient.py --init-project ... -e <low|medium|high|xhigh>`
- 默认不变：
  - `--learnbaseline` 默认仍是 `low`
  - `--init-project` 默认也改为 `low`
  - 只有显式 `-e` 时才覆盖
- 真实代码层现在已完成：
  - CLI 参数解析
  - `CodexAppClient(...)` effort 传递
  - `learn_session_baseline` / `init_project_session` 的 effort 回写
- 这轮还顺手收掉了 app-server 沙箱兼容问题：
  - `thread/start`
  - `turn/start`
  现在统一发送：
  - `approvalPolicy = "never"`
  - `sandboxPolicy = { "type": "externalSandbox", "networkAccess": "enabled" }`
- 目的不是改审批策略语义，而是把隔离委托给外部容器 / appservice 环境，避免容器内 `bwrap` / `namespace` 冲突。
- 实测：
  - `/root/a9quant-strategy` 上的 `python3 tools/appserverclient.py --learnbaseline -new -e xhigh`
  - 请求日志里已经明确带上：
    - `collaborationMode.mode = "plan"`
    - `reasoning_effort = "xhigh"`
    - `sandboxPolicy = externalSandbox`
- 当前这轮 `xhigh` baseline 仍在长时间执行中，因此 `project_config.json` 尚未完成最终回写；但请求层和事件流已证明参数已正确生效。
- 本轮再继续补了两项主线基础设施：
  - `tools/project_config.py` 的 `PLAN_TIMEOUT_SEC` 从 `1200` 提升到 `3600`
  - `tools/init.py` 现在会在新项目骨架中补齐 `docs/FOUNDATION_BRIDGE.md`
- 同时新增：
  - [sync_tools.py](/root/quant-factory-os/tools/sync_tools.py)
  作用是按固定清单把 foundation 的 `tools/` 与 `tools/prompts/` 同步到目标业务项目，不碰目标项目自己的 `tools/project_config.json`
- 已做一轮真实同步：
  - `python3 tools/sync_tools.py -p /root/a9quant-strategy`
  - a9 侧收到：
    - `docs/FOUNDATION_BRIDGE.md`
    - `appserverclient.py`
    - `project_config.py`
    - `init.py`
    - `sync_tools.py`
    - prompts 等固定清单文件
  - foundation 与 a9 两边对应 Python 文件均已编译通过

## a9quant-strategy PROJECT_GUIDE fixed question bank repair
- 本轮只修 `/root/a9quant-strategy/docs/PROJECT_GUIDE.md`，不再扩散到自动化逻辑或 runtime。
- 真实问题已经定位清楚：a9 的 `PROJECT_GUIDE` 题目标题与顺序曾被业务化改写，偏离了 foundation 固定题库；这违反了“题库结构固定、只允许项目化答案层”的规则。
- 已完成修复：
  - 保留 a9 项目的项目化开头与固定阅读顺序
  - 将 `Q1-Q17` 题面与顺序全部恢复为与 foundation 完全一致
  - 每题继续保留 `为什么问这题 / 标准答案 / 必查文件 / 查找线索 / 主线意义` 五段结构
  - 所有标准答案重新落在 a9 的业务语义上：三账本、中央银行、一期趋势/鲨鱼、当前实现边界、与 foundation 的承接方式
- 结构校验已通过：
  - 对比 foundation 与 a9 的 `Q1-Q17` 标题列表，结果完全一致
- 当前判断：
  - `a9quant-strategy/AGENTS.md`
  - `a9quant-strategy/docs/WORKFLOW.md`
  - `a9quant-strategy/docs/FILE_INDEX.md`
  与新的 `PROJECT_GUIDE` 没有明显直接冲突，因此本轮不扩大修改面。
- 随后又继续收紧了答案层，而不是继续改题库：
  - 重点修了 `Q1/Q2/Q5/Q6/Q10/Q11/Q17`
  - 这些题现在更明确地体现：
    - 终局是 `Treasury / Growth / Gamble` 三账本财富系统
    - `中央银行` 是制度化闸门/预算/权限/冻结机制，不是普通风控模块
    - 一期只能落地 B 类：趋势 + 鲨鱼
    - foundation 只承接自动化研发 OS，不覆盖业务制度本体
    - 当前主线仍是先把 owner docs 稳定成同频核心，再继续自动化与实现优化
- 在 owner 最新纠偏后，又继续重写了关键题答案，把阶段边界写清：
  - 一期不是先做完整 AI 自我迭代工厂
  - 一期主线是：中央银行总控 + 确定性策略试点 + 模拟盘/实盘接通 + 数据分析与执行数据反哺优化
  - 二期才补：`AI策略创作 -> backtesting/极限电池 -> replay仿真一致性` 这组更偏 lab 的实验室能力
  - 受这轮修正影响的重点题为：
    - `Q1`
    - `Q2`
    - `Q3`
    - `Q5`
    - `Q6`
    - `Q10`
    - `Q15`
    - `Q17`

## init-project real appserver thread
- 这一轮把 `init-project` 从本地 phase1 runtime 提升成了真实 app-server init thread。
- `python3 tools/appserverclient.py --init-project` 现在的最小产品级语义是：
  - 没有 `init_project_session` 时，不带 `-new` 也会创建新的真实 init thread
  - 已有 `init_project_session` 时，不带 `-new` 默认续跑
  - 只有显式 `-new` 才表示推翻重来
  - `-p` 是强制再走一次完整 prompt
  - 已有线程时，仅补一句 `-t` 默认是沿同一线程聊天微调，不重喂完整 prompt
- `-t` 已成为 `--instruction-text` 的短别名，并已同步到 foundation repo 与 `/root/a9quant-strategy` 最小 tools。
- `init-project` / `update-init-project` 在“需要继续推进但没有真实异常”时，现在统一返回：
  - `err_code = 0`
  - `status = needs_update`
  - `next_action = ...`
- 目标项目内的最终 prompt 仍固定落盘为：
  - `/root/a9quant-strategy/tools/init_project.final_prompt.md`
- 这份文件现在不只是审计副本，而是当前真实 init thread 的实际 turn 输入源。
- 真实验证已经通过：
  - `/root/a9quant-strategy/tools/project_config.json -> session_registry.init_project_session.thread_id` 写入了真实 app-server thread id
  - `thread_path` 写入了真实 rollout 路径
  - `last_turn_id`、`prompt_file`、`prompt_stage` 也会一起写回
- 产品级重复点击现在也有保护：
  - 如果同一 init thread 仍在进行中，重复执行 `--init-project` 不会生成第二个线程
  - 当前会返回 `err_code = 0`
  - `init_project_session_behavior = existing_thread_busy`
  - `inprogress_turn_ids = ["rollout_pending"]`
- 当前真实边界也被保留为显式事实，而不是被隐藏：
  - app-server 返回的 rollout 文件有时不会立刻落盘
  - 所以刚创建线程后立刻再次点击，可能先看到 `existing_thread_busy / rollout_pending`
  - 这属于可接受的忙态保护，不是流程错误
- 随后又补了一刀真正的 learnbaseline 对齐：
  - `init-project` 不再只起 thread/turn 就返回
  - 现在会像 `learnbaseline` 一样等待 turn 收口、等待 rollout 落盘、再读 thread 并提取最后一条 agent JSON
  - 也就是说，`init-project` 当前已经开始消费真实 plan 结果，而不是只依赖本地 phase1 payload 壳
- 同一轮还更新了 [docs/PROJECT_GUIDE.md](/root/quant-factory-os/docs/PROJECT_GUIDE.md)：
  - `Q12` 现在明确区分“未初始化项目先走 --init-project，再进入 --learnbaseline”
  - `Q16` 现在明确 `appserverclient` 有两类 thread：`init-project` init thread 和已初始化项目的 baseline/run/session 主线

## a9quant-strategy init completion
- 在 owner docs 反写完成后，已为 `/root/a9quant-strategy` 执行：
  - `python3 tools/appserverclient.py --complete-init-project`
- 真实结果：
  - `init_project_completion_status=completed`
  - `/root/a9quant-strategy/tools/project_config.json -> bootstrap_state.is_inited = "Y"`
  - `initialized_by = "appserverclient --complete-init-project"`
- 这一步没有开始 tools 迁移，也没有继续改目标项目代码；它只负责把初始化状态从未完成切到已完成。
- 现在 `/root/a9quant-strategy` 已经具备进入 `learn-baseline` 和后续主线调试的资格。

## a9quant-strategy owner docs rewrite
- 已将 `/root/a9quant-strategy` 的 6 份 owner docs 按当前正确理解重写：
  - `AGENTS.md`
  - `docs/PROJECT_GUIDE.md`
  - `docs/WORKFLOW.md`
  - `docs/ENTITIES.md`
  - `docs/FILE_INDEX.md`
  - `docs/TOOLS_METHOD_FLOW_MAP.md`
- 这次不再沿用之前偏摘要化、偏 runtime-only 的旧版本，而是按当前完成的 init-project 理解重写：
  - 文档优先级改为：总纲 -> README -> 中央银行设计 -> 一期策略手册 -> 原始想法
  - 项目阶段明确改成：研发阶段 / 上线后运维数据与持续迭代阶段
  - 协作主线明确与 foundation 对齐：learn-baseline -> 主线程 -> 角色线程 -> thread->task->run 去噪总结
  - 当前技术主线、中央银行式风险闸门、三账本终局和一期趋势+鲨鱼落地都已进入正式 owner docs
- 当前仍未执行 `--complete-init-project`，因此目标项目自己的 `bootstrap_state.is_inited` 仍保持 `N`，后续是否进入 learn-baseline 还等 owner 最后确认。

## a9quant-strategy foundation-parity owner-rules update
- 本轮把最后一组 owner 规则直接对齐到 foundation 项目本身，而不是继续补技术证据。
- 对齐内容包括：
  - 剩余初始化约定与基建项目一致
  - task/run/session 机器真相源思路与 session 审计材料保留方式与 foundation 一致
  - 准备完成后从 foundation 同款主线进入需求讨论
  - 任务完成后的收尾动作与 foundation 的 evidence + gitclient 收尾一致
- 基于这批规则，起草并回写了：
  - [learn/a9quant-strategy_init_project_update_payload_foundation_parity.json](/root/quant-factory-os/learn/a9quant-strategy_init_project_update_payload_foundation_parity.json)
- 实际执行了：
  - `python3 tools/appserverclient.py --update-init-project --payload-json learn/a9quant-strategy_init_project_update_payload_foundation_parity.json`
- 结果仍保持 fail-closed：
  - `err_code=1012`
  - `ready_for_doc_write=false`
- 但目标项目的 init session 现已推进为：
  - `answered_questions = [Q1..Q17]`
  - `unclear_questions = []`
  - `must_read_next = []`
- 到这一步，初始化理解层已经闭合；剩下的只是 owner 是否确认进入 owner docs 反写。

## a9quant-strategy owner-rules init-project update
- 本轮没有继续扫代码，而是把 owner 直接给出的规则推进到 `/root/a9quant-strategy` 的同一个 `init_project_session`。
- 规则核心包括：
  - tools 下的功能最终要下沉到目标项目自身
  - 项目分两个阶段：研发阶段；上线后的运维数据/数据分析运营/持续研发迭代阶段
  - 需求讨论与协作主线沿用基座：`learn-baseline -> 主线程 -> 角色线程 -> thread->task->run 去噪总结 -> 自循环学习`
  - 分支与交付沿用 `gitclient` 命令面
- 基于这批 owner 规则，起草并回写了：
  - [learn/a9quant-strategy_init_project_update_payload_owner_rules.json](/root/quant-factory-os/learn/a9quant-strategy_init_project_update_payload_owner_rules.json)
- 实际执行了：
  - `python3 tools/appserverclient.py --update-init-project --payload-json learn/a9quant-strategy_init_project_update_payload_owner_rules.json`
- 真实结果仍然是预期的 fail-closed：
  - `err_code=1012`
  - `ready_for_doc_write=false`
- 但目标项目的 init session 已明显推进：
  - `answered_questions = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q9", "Q10", "Q11", "Q13", "Q15", "Q16", "Q17"]`
  - 仍未闭合的只剩：
    - `Q7`
    - `Q8`
    - `Q12`
    - `Q14`
- 到这一步，后续需要的已不再是更多代码证据，而是更细的 owner 规则说明。

## a9quant-strategy init-project final technical update payload
- 继续沿 `/root/a9quant-strategy` 的同一个 `init_project_session` 推进，仍未触碰目标项目 `docs/*.md`。
- 本轮补读了最后一批 `must_read_next`：
  - `config.json`
  - `replay_runner.py`
- 这批证据已经足够确认：
  - 当前配置层仍然是 sample/sandbox 导向，显式保留了 `dry_run=true`、`live_trading=false`、sandbox/proxy defaults 等运行假设
  - `replay_runner.py` 已能把历史事件推进到主控制器的双引擎、risk approval 和执行链
- 基于这批证据，起草并回写了：
  - [learn/a9quant-strategy_init_project_update_payload_round3.json](/root/quant-factory-os/learn/a9quant-strategy_init_project_update_payload_round3.json)
- 实际执行了：
  - `python3 tools/appserverclient.py --update-init-project --payload-json learn/a9quant-strategy_init_project_update_payload_round3.json`
- 真实更新结果继续保持 fail-closed：
  - `err_code=1012`
  - `ready_for_doc_write=false`
  - `/root/a9quant-strategy/tools/project_config.json` 现已推进为：
    - `answered_questions = ["Q1", "Q2", "Q3", "Q5", "Q6", "Q10", "Q11", "Q15"]`
    - `must_read_next = []`
    - `ready_for_doc_write = false`
- 到这一步，技术补读层已基本闭合；剩余未完成项主要是 owner 规则和协作口径，而不是核心实现证据不足。

## a9quant-strategy init-project second update payload
- 继续沿 `/root/a9quant-strategy` 的同一个 `init_project_session` 推进，没有触碰目标项目 `docs/*.md`。
- 本轮补读了第二批 `must_read_next`：
  - `main_controller.py`
  - `data_synchronizer.py`
  - `account_state.py`
  - `contracts.py`
  - `test_integration.py`
  - `test_regression.py`
- 这批证据已经足够确认：
  - `main_controller.py` 是真实主控与组合根，不是占位入口
  - `data_synchronizer.py` 是状态真相源层，`account_state.py` 是建立在其上的业务账本
  - `contracts.py` 已稳定定义 `RiskRequest / TradeIntent / StrategyContext / Snapshot` 契约
  - 集成/回归测试已覆盖 live gate、trace、同步校准、OMS 幂等和 replay-driven full chain
- 基于这批证据，起草并回写了：
  - [learn/a9quant-strategy_init_project_update_payload_round2.json](/root/quant-factory-os/learn/a9quant-strategy_init_project_update_payload_round2.json)
- 实际执行了：
  - `python3 tools/appserverclient.py --update-init-project --payload-json learn/a9quant-strategy_init_project_update_payload_round2.json`
- 真实更新结果继续保持 fail-closed：
  - `err_code=1012`
  - `ready_for_doc_write=false`
  - `/root/a9quant-strategy/tools/project_config.json` 现已推进为：
    - `answered_questions = ["Q1", "Q2", "Q3", "Q5", "Q6", "Q10", "Q11"]`
    - `must_read_next = ["config.json", "replay_runner.py"]`
    - `ready_for_doc_write = false`

## a9quant-strategy init-project first update payload
- 继续沿 `/root/a9quant-strategy` 的同一个 `init_project_session` 推进，没有重跑首轮。
- 先补读了第一批 `must_read_next`：
  - `ccxt_utils.py`
  - `advanced_risk.py`
  - `trend_engine.py`
  - `shark_engine.py`
  - `base_bitget_ws.py`
  - `bitget_ws_bridge.py`
  - `market_data_hub.py`
  - `tiny_oms.py`
- 这批证据已经足够确认三件事：
  - `advanced_risk.py` 是中央银行式风控/系统模式核心，不是普通 util
  - `main workflow` 的中段已经存在：行情 -> 双引擎 intent -> RiskRequest / RiskManager -> TinyOMS -> Bitget 执行/回报
  - 核心对象边界已经能初步成立：交易所适配、风控、策略引擎、WS bridge、行情中心、OMS
- 基于这批证据，起草并回写了：
  - [learn/a9quant-strategy_init_project_update_payload.json](/root/quant-factory-os/learn/a9quant-strategy_init_project_update_payload.json)
- 实际执行了：
  - `python3 tools/appserverclient.py --update-init-project --payload-json learn/a9quant-strategy_init_project_update_payload.json`
- 真实更新结果符合预期：
  - `err_code=1012`
  - `ready_for_doc_write=false`
  - `/root/a9quant-strategy/tools/project_config.json` 已更新为：
    - `answered_questions = ["Q5", "Q6", "Q11"]`
    - 新的 `unclear_questions`
    - 新的 `customer_followups`
    - 第二批 `must_read_next = main_controller.py, data_synchronizer.py, account_state.py, contracts.py, test_integration.py, test_regression.py`

## Real a9quant-strategy init-project xhigh run
- 用真实目标项目 `/root/a9quant-strategy` 跑通了一次 session-first 初始化链，而不是继续停留在 fixture。
- 先把目标项目自己的 `tools/project_config.json` 重置为未初始化：
  - `bootstrap_state.is_inited = "N"`
  - 清空 `session_registry.init_project_session`
- 临时把 foundation 的 `tools/project_config.json -> required.project_root` 指到 `/root/a9quant-strategy`，随后执行：
  - `python3 tools/init.py`
  - `python3 tools/appserverclient.py --init-project -new --instruction-text "总纲优先，README 次之，中央银行设计是我们的亮点特色，也是风控和现金流核心；基于资管双向非对称对冲策略手册是第一期实现策略的具体内容；另外两份文档属于原始想法来源。先按17问理解，不要先写文档。"`
- 当前真实返回符合手工续跑语义：
  - `err_code=1012`
  - `ready_for_doc_write=false`
  - `answered_questions=[]`
  - `unclear_questions=Q1..Q17`
  - `customer_followups` 明确先按本轮指令校正文档优先级，再继续补读关键实现文件
  - `must_read_next` 为：
    - `ccxt_utils.py`
    - `advanced_risk.py`
    - `trend_engine.py`
    - `shark_engine.py`
    - `base_bitget_ws.py`
    - `bitget_ws_bridge.py`
    - `market_data_hub.py`
    - `tiny_oms.py`
- 更关键的是，目标项目自己的 `/root/a9quant-strategy/tools/project_config.json` 已真实写入：
  - `bootstrap_state.is_inited = "N"`
  - `session_registry.init_project_session.thread_id = init-project-20260317T142024708597Z`
  - `status = phase1_ready`
  - `effort = xhigh`
  - `session_execution_instruction` 为本轮 owner 指令
  - `customer_followups / must_read_next / ready_for_doc_write=false`
- 运行完成后，foundation 指针已恢复回 `/root/quant-factory-os`，没有把默认 `project_root` 留在外部项目上。
- 这轮也暴露了一个真实边界：`python3 tools/init.py` 在临时指向外部项目时，统一配置打印仍混入 foundation 的 bootstrap 元数据；说明 `init` 对“外部 project_root 的 bootstrap_state 归属”还没完全收干净。

## Init-project real-material-derived fixture validation
- 新增了更接近真实项目材料层级的仓库内 fixture：
  - `fixtures/init_project_real_material_fixture/README.md`
  - `fixtures/init_project_real_material_fixture/docs/总纲清单（可复制）.md`
  - `fixtures/init_project_real_material_fixture/docs/中央银行设计.md`
  - `fixtures/init_project_real_material_fixture/docs/基于资管双向非对称对冲策略手册.md`
  - `fixtures/init_project_real_material_fixture/docs/梦想中的交易资管财富系统想法.md`
  - `fixtures/init_project_real_material_fixture/docs/资管双向原始想法.md`
  - `fixtures/init_project_real_material_fixture/main_controller.py`
  - `fixtures/init_project_real_material_fixture/data_synchronizer.py`
  - `fixtures/init_project_real_material_fixture/advanced_risk.py`
  - `fixtures/init_project_real_material_fixture/contracts.py`
  - `fixtures/init_project_real_material_fixture/tiny_oms.py`
- 用这个 richer fixture 真实执行 `python3 tools/appserverclient.py --init-project -new` 后，首轮 `answered_questions` 已稳定覆盖：
  - `Q1`
  - `Q2`
  - `Q5`
  - `Q6`
  - `Q11`
- 同时系统继续保持 fail-closed：
  - `err_code=1012`
  - `ready_for_doc_write=false`
  - `customer_followups` 继续指向下一批补读文件
- 这次也暴露出一个真实边界：README 中若出现 foundation 工具调用路径，例如 `tools/appserverclient.py`，当前仍可能被记录为 `readme_refs_missing_in_repo`。
- 该误报随后已收掉：`extract_file_like_tokens()` 现在会忽略 `python3/bash/sh` 等命令上下文里的路径，因此同一 richer fixture 再次执行 `--init-project -new` 时，`readme_refs_missing_in_repo=[]`。

## Init-project Q3 evidence expansion
- 基于 richer real-material fixture 的总纲与一期策略手册，Phase 1 现在还能稳定答出 `Q3`：
  - 长期系统能力：资管财富系统与三账本治理
  - 第一落地目标：趋势 + 鲨鱼的一期策略落地
- 这次没有扩大到模糊阶段推断，只使用了两类显式证据：
  - 总纲里的终局/三账本表达
  - 一期策略手册里的趋势+鲨鱼落地表达
- 当前 richer fixture 的首轮 `answered_questions` 已稳定覆盖：
  - `Q1`
  - `Q2`
  - `Q3`
  - `Q5`
  - `Q6`
  - `Q11`

## Init-project Phase1 schema refresh
- 正式撤掉了 `--init-project` 的通用“owner docs 必须为空”强门禁口径；当前只保留 `bootstrap_state` 和 `init_project_session` 作为硬状态层。
- `init-project` Phase 1 现在明确为 `xhigh` `plan` 的 17 问理解与补缺阶段；正式输出骨架统一为：
  - `answered_questions`
  - `unclear_questions`
  - `customer_followups`
  - `document_priority_understanding`
  - `current_project_understanding`
  - `ready_for_doc_write`
- `ready_for_doc_write=true` 的语义也已收紧：只表示“17 问已基本成立，可继续在同一 session 上人工纠偏后进入写入”，不等于自动立刻写 owner docs。
- `tools/prompts/init_project_prompt.md`、`docs/WORKFLOW.md`、`docs/ENTITIES.md`、`docs/FILE_INDEX.md`、`AGENTS.md`、`tools/project_config*.json` 已同步到这套新协议。
- `tools/appserverclient.py` 的 Phase 1 运行时也已切到新方向：
  - 移除了代码里的通用 owner-doc-empty 强门禁
  - `init_project_session` 改写为记录 `answered_questions / unclear_questions / customer_followups / document_priority_understanding / current_project_understanding / ready_for_doc_write`
  - 当 `ready_for_doc_write=false` 时，`--init-project` 现在返回非零 `err_code`，但会把当前 payload 一起带回，允许在同一 session 上继续补充和纠偏

## Commands / Outputs (init-project phase1 schema refresh)
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline` -> pass
- `python3 tools/appserverclient.py --init-project` -> expected nonzero in this repo because `bootstrap_state.is_inited=Y`; this confirms the gate is still state-driven

## Init-project Phase1 fixture validation
- 新增了仓库内 fixture：
  - [README.md](/root/quant-factory-os/fixtures/init_project_fixture/README.md)
  - [project_config.json](/root/quant-factory-os/fixtures/init_project_fixture/tools/project_config.json)
- 临时把 foundation 的 `project_root` 指到这个未初始化 fixture，真实跑了一次 `python3 tools/appserverclient.py --init-project`，然后已切回 `/root/quant-factory-os`。
- 这次真实结果符合新协议：
  - 返回 `err_code=1012`
  - 同时带回 `answered_questions / unclear_questions / customer_followups / document_priority_understanding / current_project_understanding / ready_for_doc_write`
  - `customer_followups` 已能把缺口翻译成继续补读的具体文件
  - `must_read_next` 也保持在受控小集合内
- 当前已知边界也被如实暴露：
  - 第一版 `answered_questions` 过于保守，随后已继续收紧 heuristic
  - 现在同一 fixture 首轮已经能先答出 `Q1`、`Q2`、`Q5`、`Q6` 和 `Q11`
  - 后续还要继续增强 question-level reasoning，不能只停在 intake/gating 层

## What changed
- 绑定新的 active run/task，用于收敛 `run` 扶正与 `runtime_state` 唯一真相源。
- 删除 `TASKS/STATE.md` 镜像口径，改为只认 `tools/project_config.json -> runtime_state`。
- 给 `runtime_state` 增加 `current_task_id`，并允许后续过渡到“有 run、无 task”状态。
- 更新 formal mainline 文档，只保留 `project_config.json` 作为活动指针真相源。
- 调整 `tools/evidence.py` 和 `tools/gitclient.py`，不再依赖 `TASKS/STATE.md`。

## Commands / Outputs
- `python3 -m py_compile tools/project_config.py tools/gitclient.py tools/evidence.py tools/appserverclient.py` -> pass
- `python3 tools/project_config.py` -> pass; 新 `runtime_state` 输出包含 `current_task_id=task-vnext-release-baseline`
- `python3 tools/appserverclient.py --learnbaseline` -> pass; baseline 复用路径按新 `runtime_state` 工作
- `python3 tools/init.py` -> pass to completion; run/task 输出正确，最终仍因脏工作区返回 `INIT_STATUS: needs_fix`
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline` -> pass
- `make verify` -> `VERIFY: no tests/task_*.py files present; skipping pytest`

## Notes
- 历史兼容脚本仍可能保留旧 `STATE.md` 引用，本轮只收 formal mainline。

## Follow-up task
- 新建 `task-compat-shell-archive`，把 `legacy.sh` / `task.sh` / `observe.sh` / `ship.sh` 归档到 `tools/backup/`，原路径改成转发 wrapper，避免旧引用立即断裂。

## View tool stabilization
- `tools/view.sh` 已改成稳定的 Python 实现，但保留原工具路径，避免正式阅读协议继续漂移。
- 现在同时支持 `tools/view.sh ...` 和 `python3 tools/view.sh ...`，并兼容历史 `--lines START:END`。
- 新增标准库回归测试 `tests/test_view_tool.py`，覆盖范围读取、`--find`、repo 边界和 denylist。

## Commands / Outputs (view tool stabilization)
- `python3 -m py_compile tools/view.sh` -> pass
- `tools/view.sh AGENTS.md --from 1 --to 3` -> pass

## foundation bridge template + mainline denoise
- 当前主线已经确认：foundation 已开始在真实业务项目中做试点接入，但自动化主线还没有完全闭合。
- 当前更准确的工程现实是：
  - `Codex` 负责更强的手工调试和即时接管
  - foundation 负责更强的自动化研发执行与交付沉淀
  - 两者仍然需要并用，而不是假装已经进入全自动阶段
- 为了避免 foundation 与业务项目关系散落在多个主线文档里，本轮将这部分解释统一收口为：
  - `docs/FOUNDATION_BRIDGE.md`
- 这份模板当前固定回答：
  - foundation 是什么
  - foundation 有什么用
  - 为什么使用它
  - foundation 和业务项目的关系
  - foundation 包含哪些文档、命令和运行产物
  - 我们当前的开发模式是什么
- 同时对主线文档只做了最小改动：
  - `docs/PROJECT_GUIDE.md` 的 `Q2` 补清“已试点接入，但自动化未完全闭合”
  - `docs/WORKFLOW.md` 补清“当前仍是 Codex 手工调试 + foundation 自动化一起推进”
  - `docs/FILE_INDEX.md` 将 `docs/FOUNDATION_BRIDGE.md` 纳入 owner docs 入口
- 随后又把 `docs/FOUNDATION_BRIDGE.md` 重写得更短更硬，并明确写死：
  - `quant-factory-os` 是仓库名
  - `foundation` 是这个仓库对外提供的角色名
  - 这样业务项目接入时不会再把仓库名和角色名混成一个概念
- `python3 tools/view.sh AGENTS.md --from 1 --to 3` -> pass
- `python3 tools/view.sh AGENTS.md --lines 1:3` -> pass
- `tools/view.sh AGENTS.md --find '^## 0' --context 1` -> pass
- `python3 -m unittest -q tests.test_view_tool` -> pass

## View usage docs sync
- `docs/WORKFLOW.md` 和 `docs/PROJECT_GUIDE.md` 现在明确写了 `tools/view.sh` 是正式文件读取入口，并支持直接执行与 `python3` 调用。
- `README.md` 新增了最小 `tools/view.sh` 示例，方便后续按统一方式阅读仓库长文件。

## Commands / Outputs (view usage docs sync)
- `python3 tools/view.sh docs/PROJECT_GUIDE.md --from 1 --to 12` -> pass
- `python3 tools/view.sh docs/WORKFLOW.md --from 1 --to 18` -> pass
- `python3 tools/view.sh README.md --from 1 --to 20` -> pass

## Compatibility archive update
- 已创建 `tools/backup/`，并把 `legacy.sh` / `task.sh` / `observe.sh` / `ship.sh` 迁入归档目录。
- 原 `tools/*.sh` 路径现在只保留最小 wrapper，执行时先打印 deprecated 提示，再转发到 `tools/backup/`。
- formal mainline 文档已同步说明这些 shell 入口只是过渡兼容层。

## Task JSON bootstrap
- 新增 `TASKS/QUEUE.json` 作为 queue 机器真相源，当前只覆盖 active/open 工作项。
- 新增 `TASKS/TASK-vnext-release-baseline.json` 与 `TASKS/TASK-compat-shell-archive.json` 作为当前 run 下 task 真相源。
- `tools/project_config.json` 新增 `runtime_state.current_task_json_file` 和 `task_registry`，把 task/queue JSON 指针写死到运行时配置。
- `TASKS/*.md` 和 `TASKS/QUEUE.md` 现在只保留迁移期人类可读视图。

## Python archive update
- `tools/run_a9.py` 已归档到 `tools/backup/run_a9.py`；当前仓库未发现正式入口引用它。

## Active task shift
- 当前 active task 已切到 `task-task-queue-json-bootstrap`，用于承接 `task.json / queue.json` 机器真相源和 `runtime_state.current_task_json_file` 的引入。

## Taskstore bootstrap
- 新增 `tools/taskstore.py`，提供 active task、指定 task、queue 和 `run_id -> task_id` 的统一 JSON 读取入口。
- `tools/evidence.py` 已先切到 `taskstore.find_task_id_for_run()`，验证公共层可以服务现有主线工具。
- 当前 active task 已继续切到 `task-taskstore-bootstrap`。

## Active task shift
- 当前 active task 已切到 `task-gitclient-taskstore-integration`，用于承接 `gitclient` 对 task JSON 的接入。

## Gitclient taskstore integration
- `tools/gitclient.py` 的 `resolve_commit_message()` 现在优先读取 active task JSON。
- 当前优先级变为：显式 `--commit` message -> active task JSON 的 `title/task_id` -> `runtime_state.current_task_file/current_task_id` -> `current_run_id` -> 时间戳 fallback。

## Appserverclient taskstore integration
- `tools/appserverclient.py` 现在会通过 `taskstore` 读取 active task JSON。
- `APP_RUNTIME_STATE_*` 之后会追加 `APP_ACTIVE_TASK_*` 日志块，显式打印当前 `task_id/title/status/run_id`。
- 这一步只补 task 上下文感知，不改 learn/fork/current-turn 的 app-server 调用顺序。

## Taskclient bootstrap
- 新增 `tools/taskclient.py --pick-next`，先承担 Python-first 的 queue 选择和 runtime 绑定职责。
- `tools/taskstore.py` 新增 queue 写回和 active task 绑定能力，供 `taskclient` 复用。
- 这一步只替代旧 `task.sh` 的最小核心职责，不接 ship/PR。

## Taskclient create-task
- `tools/taskclient.py` 新增 `--create-task`，可以直接生成 `TASKS/TASK-*.json` 和兼容 `md` 视图。
- 新入口支持可选 `--queue`，把新 task 追加进 `TASKS/QUEUE.json`。
- 这一步仍保持最小参数模型：`title / goal / scope / run_id`。
- 为验证路径已实际生成 `TASKS/TASK-bootstrap-sample-task.json` / `TASKS/TASK-bootstrap-sample-task.md`，并追加 `queue-bootstrap-sample-task` 到 `TASKS/QUEUE.json`。

## Taskclient schema tightening
- `TASKS/_SCHEMA.task.json` 已补齐 `risks` / `rollback_plan`，与当前 task payload 对齐。
- `taskclient --create-task` 现在支持 `--priority --non-goal --input --acceptance --risks --rollback-plan`，并带最小字段校验与重复 slug 保护。
- `taskstore.save_queue()` 现在会自动刷新 `QUEUE.json.updated_at`。

## Taskclient create-task UX
- `create-task` 现在默认复用当前 runtime run，不再强制每次显式传 `--run-id`。
- `--scope --input --non-goal --acceptance` 现在支持重复传参和逗号分隔。
- 新增 `--activate`，创建后可以直接把新 task 绑定成 active task。
- 已用 `TASKS/TASK-ux-sample-task.json` 做真实验证，确认 `--activate` 生效；验证后已把 runtime 指针切回本轮正式任务，避免后续上下文漂移。

## Task wrapper reroute
- `tools/task.sh --next` 和 `tools/task.sh --pick queue-next` 现在直接转到 `python3 tools/taskclient.py --pick-next`。
- 其他参数仍会回退到 `tools/backup/task.sh`，所以这一刀只是把主线路径从 shell wrapper 上移开，不是一次性硬删兼容链。
- 已用真实 `bash tools/task.sh --next` 验证 reroute 生效；验证后把样例 queue item 恢复到 `pending`，并把 runtime 指针切回本轮正式任务，避免样例任务继续占住上下文。

## Taskclient unify entry
- 当前 active task 已切到 `task-taskclient-unify-entry`，用于承接 `taskstore -> taskclient` 合并和 `task.sh` 直接弃用。
- `tools/taskclient.py` 现在同时承接 task/queue JSON 的公共读写、queue 选择、active task 读取与 task bootstrap；对外主命令收口为 `--next` 和 `--create`。
- `tools/appserverclient.py`、`tools/gitclient.py`、`tools/evidence.py` 已改为直接从 `taskclient` 导入 task 读取能力，不再依赖独立 `taskstore` 入口。
- `tools/taskstore.py` 已降级成兼容转发模块，历史实现归档到 `tools/backup/taskstore.py`；`tools/task.sh` 现在直接报废弃并退出，不再回退到 `tools/backup/task.sh`。
- 本轮 gate 中 `python3 tools/appserverclient.py --fork-current` 仍被 `/root/.codex/sessions` 权限阻塞，错误为 `permission denied`；这次本地重构未依赖该步骤。

## Commands / Outputs (compatibility archive)
- `bash tools/legacy.sh --help || true` -> pass; wrapper 生效并转发到 `tools/backup/legacy.sh`
- `python3 tools/project_config.py` -> pass; `runtime_state.current_task_id=task-compat-shell-archive`，`current_task_file=TASKS/TASK-compat-shell-archive.md`
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline` -> pass

## Legacy entrypoint archive cleanup
- 当前 active task 已切到 `task-archive-legacy-tool-entrypoints`，只做正式 `tools/` 白名单清理。
- 旧入口已从 `tools/` 顶层移出并归档到 `tools/backup/`：
  - `learn.py`
  - `ready.py`
  - `orient.py`
  - `choose.py`
  - `council.py`
  - `arbiter.py`
  - `slice_task.py`
  - `run_main.py`
- 旧 shell 顶层入口也已移出正式层，wrapper 版本归档到：
  - `tools/backup/legacy.wrapper.sh`
  - `tools/backup/observe.wrapper.sh`
  - `tools/backup/ship.wrapper.sh`
  - `tools/backup/task.wrapper.sh`
- 正式主流程现阶段只保留：
  - `tools/init.py`
  - `tools/appserverclient.py`
  - `tools/gitclient.py`
  - `tools/taskclient.py`
  - `tools/project_config.py`

## Run-main escalation resolution
- task 机器层新增：
  - `task_summary.run_main_resolution_policy`
  - `task_summary.run_main_resolution`
- `tools/taskclient.py` 新增最小入口：
  - `--run-main-resolution`
  - `--set-run-main-resolution`
  - `--refresh-run-main-resolution`
- 当前最小状态约定是：
  - `not_needed`
  - `pending_ack`
  - `acknowledged`
  - `closed`
- 当前最小关闭条件是：
  - 已存在 `run-main` summary
  - `test_gate` 已通过
  - 没有 blocking issue
- 已用 `TASKS/TASK-run-main-escalation-resolution.json` 做真实验证，确认：
  - 初始升级状态可刷新为 `pending_ack`
  - 在 `run-main` summary 存在且 `test_gate=passed` 后，可手动写回 `close_escalation=true`

## Commands / Outputs (run-main escalation resolution)
- `python3 -m py_compile tools/taskclient.py` -> pass
- `python3 tools/taskclient.py --refresh-task-gaps --task-json-file TASKS/TASK-run-main-escalation-resolution.json` -> pass
- `python3 tools/taskclient.py --refresh-task-escalation --task-json-file TASKS/TASK-run-main-escalation-resolution.json` -> pass
- `python3 tools/taskclient.py --refresh-run-main-resolution --task-json-file TASKS/TASK-run-main-escalation-resolution.json` -> pass; 首次返回 `status=pending_ack`
- `python3 tools/taskclient.py --set-role-summary --task-json-file TASKS/TASK-run-main-escalation-resolution.json --role run-main ...` -> pass
- `python3 tools/taskclient.py --set-test-gate --task-json-file TASKS/TASK-run-main-escalation-resolution.json --gate-status passed --gate-evidence "manual verification demo"` -> pass
- `python3 tools/taskclient.py --set-run-main-resolution --task-json-file TASKS/TASK-run-main-escalation-resolution.json --resolution-status closed --resolution-note "run-main manually closed resolved escalation." --close-escalation` -> pass
- `python3 tools/taskclient.py --run-main-resolution --task-json-file TASKS/TASK-run-main-escalation-resolution.json` -> pass; 最终返回 `status=closed`、`close_escalation=true`
- owner docs 已同步到这条主流程白名单，`AGENTS.md`、`docs/WORKFLOW.md`、`docs/FILE_INDEX.md` 不再把上述旧入口放在正式工具面。

## Commands / Outputs (legacy entrypoint archive)
- `python3 tools/taskclient.py --create --title "archive legacy tool entrypoints" ... --activate` -> pass
- `python3 tools/taskclient.py --active-task` -> pass; active task 切到 `task-archive-legacy-tool-entrypoints`
- `python3 tools/project_config.py` -> pass; `runtime_state.current_status=completed`

## Appserverclient summarize / refresh loop
- 当前 active task 已切到 `task-appserverclient-summarize-refresh-baseline-loop`，目标是补齐 current summary 与 baseline refresh 的正式入口。
- `tools/appserverclient.py` 现已新增：
  - `--summarize-current`
  - `--refresh-baseline`
- `tools/project_config.py` 新增 `update_current_summary()`，把 current summary 的来源 thread、摘要正文和 baseline refresh 结果统一写回 `session_registry.current_summary`。
- 真实链路已打通：
  - `--summarize-current` 会在 current fork 上发 summarize prompt，抽取最后一条 agent message，并写回 `session_registry.current_summary.summary_text`
  - `--refresh-baseline` 会只消费 `session_registry.current_summary`，在 baseline thread 上做增量 refresh，并把结果写回 `baseline_refresh_text`

## Commands / Outputs (appserverclient summarize / refresh)
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py` -> pass
- `python3 tools/appserverclient.py --summarize-current` -> pass; 输出 `current_summary_text_start ... current_summary_text_end`
- `python3 tools/appserverclient.py --refresh-baseline` -> pass; 输出 `baseline_refresh_text_start ... baseline_refresh_text_end`
- `python3 tools/project_config.py` -> pass; `session_registry.current_summary` 已包含 `thread_id/thread_path/status/source/model/effort`

## Entity layering clarifications
- 新建并完成 `task-entity-layering-clarifications`，只做 owner docs 最小口径收紧，不改代码结构。
- `docs/ENTITIES.md` 现在显式引入 `baseline` 和 `thread summary` 两层，明确推荐链路是 `thread summary -> task summary -> run evidence / run summary -> baseline refresh`。
- 当前实现被明确标注为过渡态：
  - `session_registry.current_summary` 是 thread-level transitional summary
  - `reports/<RUN_ID>/summary.md` 和 `decision.md` 目前仍偏 active task evidence，属于 run 容器下的 task-focused 表达
- `docs/WORKFLOW.md` 现在也明确：
  - `--summarize-current` 产出当前 thread 的去噪摘要
  - `--refresh-baseline` 当前直接消费 `current_summary`
  - 长期 baseline 应优先吸收 run-level stable summaries，而不是直接吸收原始 thread 噪音

## Task summary bootstrap
- 新建并完成 `task-task-summary-bootstrap`，把 task-level aggregate summary 收为 `TASKS/TASK-*.json` 内的稳定对象 `task_summary`，不额外拆独立文件。
- `TASKS/_SCHEMA.task.json` 已新增 `task_summary.status/key_updates/decisions/risks/verification/next_steps/source_threads/updated_at`。
- `tools/taskclient.py` 已新增：
  - `--task-summary`
  - `--set-task-summary`
- `write_task_md()` 现在会把 `task_summary` 渲染到 `TASKS/TASK-*.md` 的 `## Task Summary` 区块，保持 `json truth + md view`。
- 真实验证已通过：
  - `python3 -m py_compile tools/taskclient.py`
  - `python3 tools/taskclient.py --set-task-summary ...`
  - `python3 tools/taskclient.py --task-summary`

## Run summary bootstrap
- 新建并完成 `task-run-summary-bootstrap`，把 run-level aggregate machine truth 收到 `reports/<RUN_ID>/run_summary.json`，不去污染 `project_config.json`。
- 新增 [reports/_SCHEMA.run_summary.json](/root/quant-factory-os/reports/_SCHEMA.run_summary.json) 作为最小 schema 模板。
- `tools/evidence.py` 现在在 `make evidence RUN_ID=...` 时会自动确保 `run_summary.json` 存在。
- 当前设计已经明确分层：
  - `run_summary.json` 是机器真相源
  - `summary.md / decision.md` 继续是 run 级 md 视图
- 真实验证已通过：
  - `python3 -m py_compile tools/evidence.py`
  - `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline`
  - `reports/run-2026-03-11-vnext-release-baseline/run_summary.json` 已自动生成

## Run summary writeback entry
- 新建并完成 `task-run-summary-writeback-entry`，没有新增 `runclient`，而是把 `run_summary.json` 的最小读写入口直接落在 `tools/evidence.py`。
- 新增命令：
  - `python3 tools/evidence.py --run-id <RUN_ID> --run-summary`
  - `python3 tools/evidence.py --run-id <RUN_ID> --set-run-summary ...`
- 已用真实命令把 [run_summary.json](/root/quant-factory-os/reports/run-2026-03-11-vnext-release-baseline/run_summary.json) 写成一版稳定内容，并成功读回。
- 这一步只补 run-level machine truth 的写回，不改 baseline 仍然只消费 `current_summary` 的现状。

## Run summary reconciliation
- 新建并完成 `task-run-summary-aggregation-reconciliation`，把 `run_summary.json` 的 `active_tasks/completed_tasks/source_tasks` 收敛到按同一 `run_id` 下 `TASKS/TASK-*.json` 真相源重算。
- `tools/evidence.py` 新增：
  - `python3 tools/evidence.py --run-id <RUN_ID> --reconcile-run-summary`
- 这一步修掉了 `run_summary.json` 中把已完成 task 继续留在 `active_tasks` 的手工漂移，但也真实暴露了历史遗留的多个 `active` task；当前策略是不在 run 层掩盖它，而是把它作为后续 task 真相源清理输入。

## Commands / Outputs (run summary reconciliation)
- `python3 -m py_compile tools/evidence.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --reconcile-run-summary` -> pass; `task-run-summary-writeback-entry` 已从 `active_tasks` 移除
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary` -> pass; 当前 `active_tasks` 直接反映 task JSON 中仍为 `active` 的遗留项

## Stale active task truth cleanup
- 新建并完成 `task-stale-active-task-truth-cleanup`，直接清理 `TASKS/*.json` 中 6 个历史遗留 `active` 条目。
- 本轮只做最小状态修正，不重写历史实现内容：
  - `task-appserverclient-role-thread-fork-binding`
  - `task-appserverclient-role-turn-command`
  - `task-bootstrap-sample-task`
  - `task-schema-sample-task`
  - `task-taskclient-unify-entry`
  - `task-ux-sample-task`
- 清理后重新运行 `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --reconcile-run-summary`，当前 `run_summary.json.active_tasks=[]`，`run_summary.json.status=completed`。

## Commands / Outputs (stale active task truth cleanup)
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --reconcile-run-summary` -> pass; `active_tasks=[]`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary` -> pass; `status=completed`

## Run summary baseline refresh automation boundary
- 新建并完成 `task-run-summary-baseline-refresh-automation-boundary`，把 `refresh-baseline` 的输入选择从隐式 fallback 收成显式边界。
- `tools/appserverclient.py` 现在会先通过 helper 选择 baseline refresh 输入，并在 `session_registry.current_summary` 回写：
  - `baseline_refresh_input_type`
  - `baseline_refresh_input_ref`
- 本轮同时修正了 [tools/refresh_baseline_prompt.md](/root/quant-factory-os/tools/refresh_baseline_prompt.md) 的口径，使其明确“优先消费 run_summary，缺失时才回退 current_summary”。

## Commands / Outputs (run summary baseline refresh automation boundary)
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py` -> pass
- `python3 tools/appserverclient.py --refresh-baseline` -> pass; 实际输出 `baseline_refresh_input_type=run_summary`
- `python3 tools/project_config.py` -> pass; `session_registry.current_summary` 已更新，来源仍为 `refresh_baseline_main`

## Run summary semantic compaction
- 新建并完成 `task-run-summary-semantic-compaction`，把 run-level 宽表压缩成更短的 `baseline_ready_summary`，专门供 baseline refresh 使用。
- `tools/evidence.py` 新增：
  - `python3 tools/evidence.py --run-id <RUN_ID> --compact-run-summary`
- `tools/appserverclient.py` 的 `refresh-baseline` 现在在存在 `baseline_ready_summary` 时，优先把这段压缩块放进 prompt，而不再展开整份 `completed/source/verification` 宽列表。

## Run summary risk near-duplicate merge policy
- 新建并完成 `task-run-summary-risk-near-duplicate-merge-policy`，只收 `cross_task_risks` 里的近义 blocked-gate 风险句，不扩别的层。
- `tools/evidence.py` 新增了一个很窄的规则：如果 `cross_task_risks` 同时存在通用 `test gate remains blocked` 和更具体的 blocked-gate 解释句，则只保留更具体的 run-level 风险表达。
- 证据粒度没有被挤压到风险字段里；`verification_overview` 继续保留底层验证命令和 task 级证据前缀。
- 重新执行 `--normalize-run-summary` 后，当前 `run_summary.json.cross_task_risks` 已从两条 blocked-gate 近义句收成一条更具体的 run-level 风险句。

## Commands / Outputs (run summary risk near-duplicate merge policy)
- `python3 -m py_compile tools/evidence.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --normalize-run-summary` -> pass; `cross_task_risks` 中通用 blocked-gate 句被更具体的解释句吸收
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary` -> pass; 当前风险字段只保留一条 blocked-gate run-level 风险表达
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline` -> pass

## Appserverclient task-rule boundary tightening
- 新建并完成 `task-appserverclient-task-rule-boundary-tightening`，只做一刀最小解耦，不改 formal mainline。
- `tools/taskclient.py` 新增内部统一入口 `refresh_task_coordination(task_json_file, include_role_merge=...)`，把 task 层的：
  - role summary merge
  - gap refresh
  - escalation refresh
  - run-main resolution refresh
  收到同一个 task-side helper。
- `tools/appserverclient.py` 不再显式串四个 task 规则函数：
  - `--summarize-role` 现在统一调用 `refresh_task_coordination(..., include_role_merge=True)`
  - `--mark-test-gate` 现在统一调用 `refresh_task_coordination(..., include_role_merge=False)`
- 这一步的价值是让 runtime 知道“何时刷新 task 协调状态”，但不再知道“怎么一步步刷新”，从而把 task policy 继续压回 `taskclient`。

## Commands / Outputs (appserverclient task-rule boundary tightening)
- `python3 -m py_compile tools/appserverclient.py tools/taskclient.py` -> pass
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline` -> pass

## Appserverclient task-policy boundary tightening pass 2
- 新建并完成 `task-appserverclient-task-policy-boundary-tightening-pass-2`，继续只做一刀最小解耦，不改 formal mainline。
- `tools/taskclient.py` 新增内部 helper `update_role_summary_with_task_links()`，统一承接：
  - `role_summaries.<role>` 写回
  - `task_summary.role_summary_evidence`
  - `task_summary.source_threads`
- `tools/appserverclient.py --summarize-role` 不再直接调用 `update_task_summary()` 去改 task aggregate 字段，而是只调用 task-side helper，再继续走 `refresh_task_coordination(...)`。
- 这一步的价值是让 runtime 不再直接知道 role summary 和 task aggregate 之间的联动写法，进一步把 task policy 压回 `taskclient`。

## Commands / Outputs (appserverclient task-policy boundary tightening pass 2)
- `python3 -m py_compile tools/appserverclient.py tools/taskclient.py` -> pass
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline` -> pass

## Appserverclient task-policy boundary tightening pass 3
- 新建并完成 `task-appserverclient-task-policy-boundary-tightening-pass-3`，继续只做一刀最小解耦，不改 formal mainline。
- `tools/taskclient.py` 新增 `update_test_gate_from_test_summary()`，统一承接：
  - 读取 `role_summaries.test`
  - 拼接 `test-summary-turn:*` / `test-thread:*` 证据
  - 写回 `test_gate`
- `tools/appserverclient.py --mark-test-gate` 不再直接读取 `role_summaries.test` 并手工拼装证据，而是只调用 task-side helper，再继续走 `refresh_task_coordination(...)`。
- 这一步的价值是让 runtime 不再直接知道 test 证据如何组装，继续把 task policy 压回 `taskclient`。

## Commands / Outputs (appserverclient task-policy boundary tightening pass 3)
- `python3 -m py_compile tools/appserverclient.py tools/taskclient.py` -> pass
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline` -> pass

## Appserverclient task-policy touchpoint audit
- 新建并完成 `task-appserverclient-task-policy-touchpoint-audit`，只做短审计，不再继续硬拆第四刀。
- 当前剩余触点主要是：
  - `load_active_task()`：用于拿当前 task id/json file，属于 runtime 入口定位所必需
  - `get_role_threads()` / `update_role_thread()`：用于 role thread 真实绑定与读取，属于 runtime 事实写回
  - `update_role_summary_with_task_links()` / `update_test_gate_from_test_summary()` / `refresh_task_coordination()`：已经是 task-side helper 调用，不再是 runtime 自己理解 policy
- 结论是：剩余触点大多已经是 runtime 必需，而不是 task policy 泄漏；继续硬拆会让调用链更长、定位更差。

## Commands / Outputs (appserverclient task-policy touchpoint audit)
- `grep -nE "load_active_task|get_role_threads|update_role_thread|update_role_summary_with_task_links|update_test_gate_from_test_summary|refresh_task_coordination" tools/appserverclient.py` -> pass
- `tools/view.sh tools/appserverclient.py --from 836 --to 1001` -> pass

## Shortest stable mainline documentation
- 新建并完成 `task-shortest-stable-mainline-documentation`，把当前最短稳定主线明确写进 owner docs。
- [docs/WORKFLOW.md](/root/quant-factory-os/docs/WORKFLOW.md) 现在新增 `Shortest Stable Mainline`，只保留：
  - `init`
  - `learnbaseline`
  - 明确 run 方向
  - `fork-current`
  - 按需 `fork-role/role-turn/summarize-role/mark-test-gate`
  - `summarize-current`
  - `refresh-baseline`
  - `gitclient --commit`
- [docs/FILE_INDEX.md](/root/quant-factory-os/docs/FILE_INDEX.md) 也新增同一条简化操作面，明确“没有真实多角色需要时，不要额外引入 role thread 步骤”。

## Commands / Outputs (shortest stable mainline documentation)
- `python3 -m py_compile tools/appserverclient.py tools/taskclient.py tools/evidence.py tools/gitclient.py` -> pass
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline` -> pass

## Commands / Outputs (run summary semantic compaction)
- `python3 -m py_compile tools/evidence.py tools/appserverclient.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --compact-run-summary` -> pass; `run_summary.json` 已新增 `baseline_ready_summary`
- `python3 tools/appserverclient.py --refresh-baseline` -> pass; 实际请求体已切到 `run_summary -> baseline_ready_summary` 压缩块

## Baseline-ready summary quality
- 新建并完成 `task-baseline-ready-summary-quality`，继续只提升 `baseline_ready_summary` 的表达质量。
- `tools/evidence.py` 现在会对常见 `task-...:` 前缀和工具路径表述做最小规范化，因此 `baseline_ready_summary` 已从“机械前缀堆叠”收成更接近 run-level prose 的短摘要。

## Commands / Outputs (baseline-ready summary quality)
- `python3 -m py_compile tools/evidence.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --compact-run-summary` -> pass; `baseline_ready_summary` 已更新成更自然表述
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary` -> pass; 可见新的 prose-like `baseline_ready_summary`

## Short stable mainline regression
- 新建并完成 `task-short-stable-mainline-regression`，只验证当前最短稳定主线，不扩结构，也不引入 role thread。
- 本轮真实执行了：
  - `python3 tools/init.py`
  - `python3 tools/appserverclient.py --learnbaseline`
  - `python3 tools/appserverclient.py --fork-current`
- 结论是：
  - `learnbaseline` 在当前环境直接通过
  - `fork-current` 在当前沙箱中会因 `/root/.codex/sessions` 访问受限而失败
  - 同一命令在提权后通过，并成功写回新的 `fork_current_session`
- 这说明当前最短稳定主线的 repo 逻辑仍然成立；本轮暴露的是环境权限差异，而不是 formal mainline 失效。

## Commands / Outputs (short stable mainline regression)
- `python3 tools/init.py` -> started normally; visible `INIT_STEP[...]` output observed
- `python3 tools/appserverclient.py --learnbaseline` -> pass
- `python3 tools/appserverclient.py --fork-current` -> sandbox permission denied on `/root/.codex/sessions`
- escalated `python3 tools/appserverclient.py --fork-current` -> pass; `fork_current_thread_id=019ce7a6-464f-7d52-8820-1a8c4376933f`

## Codex Full Access runtime prerequisite
- 新建并完成 `task-codex-full-access-runtime-prerequisite`，只补最小运行前提说明，不改 formal mainline。
- 本轮确认：在 Codex TUI 的 `Default` 权限模式下，真实 `baseline / fork-current / summarize-current / refresh-baseline` 调试会受 workspace 外 `/root/.codex/sessions` 边界影响；切到 `/permissions -> Full Access` 后，这条真实 session 链恢复正常。
- 这条说明已同步到 [docs/WORKFLOW.md](/root/quant-factory-os/docs/WORKFLOW.md) 和 [docs/FILE_INDEX.md](/root/quant-factory-os/docs/FILE_INDEX.md)，定位为运行前提，而不是主线逻辑修复。

## Commands / Outputs (Codex Full Access runtime prerequisite)
- `python3 tools/appserverclient.py --fork-current` -> pass under Codex TUI `Full Access`; `fork_current_thread_id=019ce7b4-c653-79c3-8482-eacc971679cf`
- `python3 tools/appserverclient.py --summarize-current` -> pass; `current_summary_text_start ... current_summary_text_end`
- `python3 tools/appserverclient.py --refresh-baseline` -> pass; `baseline_refresh_input_type=run_summary`

## Task / queue truth reconciliation cleanup
- 新建并完成 `task-task-queue-truth-reconciliation-cleanup`，专门收口 `runtime_state`、`TASKS/QUEUE.json` 和 `TASKS/TASK-*.json` 之间的历史状态漂移。
- `tools/taskclient.py` 新增 `--reconcile-task-queue-truth`，统一完成三件事：
  - 把旧 `done` 状态归一成 `completed`
  - 把非当前的陈旧 `active` task 收回到 `completed` 或 `pending`
  - 把 `QUEUE.json` 的历史 `active/pending` 条目按 task 真相源重算
- 当前收口后：
  - `TASKS/QUEUE.json` 已无遗留未完成项
  - 当前唯一 active task 只剩本轮收口 task
  - `TASKS/QUEUE.md` 已缩成废弃兼容说明页，不再保留会误导自动化的旧 backlog 文本
- owner docs 口径同步更新：
  - `AGENTS.md`
  - `docs/PROJECT_GUIDE.md`
  - `docs/WORKFLOW.md`
  - `docs/FILE_INDEX.md`

## Commands / Outputs (task / queue truth reconciliation cleanup)
- `python3 -m py_compile tools/taskclient.py` -> pass
- `python3 tools/taskclient.py --reconcile-task-queue-truth` -> pass; normalized historical task statuses and queue item statuses
- `python3 tools/project_config.py` -> pass; `current_task_id=task-task-queue-truth-reconciliation-cleanup`

## Run summary stale prose cleanup
- 新建并完成 `task-run-summary-stale-prose-cleanup`，只收仍然落后于当前代码现实的 run-level 风险句和 next-step 句。
- `tools/evidence.py` 的 `normalize-run-summary` 现在会把两类已过时表述改写成当前事实：
  - `baseline still does not consume run summary yet`
  - `connect baseline refresh to run summary after this stabilizes`
- 当前 [run_summary.json](/root/quant-factory-os/reports/run-2026-03-11-vnext-release-baseline/run_summary.json) 已更新成：
  - `baseline refresh now consumes run summary by default; remaining work is to keep run-level prose aligned with current truth`
  - `continue tightening run-level prose so baseline-ready summaries stay aligned with current code and runtime truth`
- 这一步没有扩新功能，只把 evidence 语义重新拉回当前真实主线。

## Commands / Outputs (run summary stale prose cleanup)
- `python3 -m py_compile tools/evidence.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --normalize-run-summary` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --compact-run-summary` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary` -> pass; stale baseline-consumption and next-step prose removed

## Run summary risk layering cleanup
- `normalize-run-summary` 现在会把 run-level 风险分成两层：
  - `cross_task_risks`：当前主线仍成立的运行风险
  - `audit_risks`：历史清理、审计残留、兼容资产风险
- `baseline_ready_summary` 继续只消费 `cross_task_risks`，不会把 audit-only 噪音带入 baseline-facing compaction。

## Commands / Outputs (run summary risk layering cleanup)
- `python3 -m py_compile tools/evidence.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --normalize-run-summary` -> pass; 审计/历史风险已分流到 `audit_risks`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --compact-run-summary` -> pass; `baseline_ready_summary` 仍只包含主线运行风险
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary` -> pass

## Tool surface and prompt asset cleanup
- `tools/prompts/` 已建立，正式 prompt 模板已从 `tools/` 顶层迁入：
  - `learnbaseline_prompt.md`
  - `summarize_current_prompt.md`
  - `summarize_role_prompt.md`
  - `refresh_baseline_prompt.md`
- 传统需求分析材料已从 `tools/` 迁到 `chatlogs/需求管理及分析工作指南.doc`。
- `TOOLS_METHOD_FLOW_MAP.md` 已迁到 `docs/TOOLS_METHOD_FLOW_MAP.md`。
- 顶层 `tools/start.sh` 与 `tools/onboard.sh` 已归档到 `tools/backup/`，不再占据正式工具面。
- 正式主线引用已同步到新路径；历史 task / learn artifacts 保留旧路径作为审计痕迹，不做批量重写。

## Commands / Outputs (tool surface and prompt asset cleanup)
- `python3 -m py_compile tools/project_config.py tools/appserverclient.py` -> pass
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline` -> pass

## Unused top-level tool artifact cleanup
- 删除了未被正式主线引用的 `tools/console.txt`。
- 顶层 `tools/taskstore.py` 与 `tools/sync_exam.py` 已迁到 `tools/backup/`：
  - `tools/backup/taskstore.forwarder.py`
  - `tools/backup/sync_exam.py`
- `tools/slice.py` 保留在顶层，因为 `make slice` 仍然直接依赖它。

## Commands / Outputs (unused top-level tool artifact cleanup)
- `grep -RIn "slice\\.py\\|sync_exam\\.py\\|taskstore\\.py" Makefile AGENTS.md README.md docs tools --exclude-dir=.git --exclude-dir=backup` -> confirmed only `slice.py` is still used by `Makefile`
- `python3 -m py_compile tools/project_config.py tools/appserverclient.py` -> pass
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline` -> pass

## Unused shell helper and Make target cleanup
- 顶层 `tools/doctor.sh`、`tools/enter.sh`、`tools/smoke.sh` 已归档到 `tools/backup/`。
- `Makefile` 保留，但已删掉失效的 `doctor / awareness / ship / orchestrator` targets。
- 保留的正式 targets 现在只聚焦：
  - `make evidence`
  - `make verify`
  - `make slice`

## Commands / Outputs (unused shell helper and Make target cleanup)
- `python3 -m py_compile tools/project_config.py tools/appserverclient.py` -> pass
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline` -> pass
- `make verify` -> no tests present; skipped pytest as expected

## Baseline prefers run summary
- 新建并完成 `task-baseline-prefers-run-summary`，把 `appserverclient --refresh-baseline` 的输入优先级改为：
  - `reports/<RUN_ID>/run_summary.json`
  - `session_registry.current_summary`（仅缺失时回退）
- 真实运行 `python3 tools/appserverclient.py --refresh-baseline` 后，`turn/start` 请求体中已经出现 `run_summary:` 段，而不是 `current_summary:` 段，说明输入优先级生效。
- 本轮没有改 baseline writeback 的输出落点，仍然回写到 `session_registry.current_summary.baseline_refresh_text`。

## Project guide requirement-analysis principles
- 新建并完成 `task-project-guide-requirement-analysis-principles`，把 [tools/需求管理及分析工作指南.doc](/root/quant-factory-os/tools/需求管理及分析工作指南.doc) 中适合 AI/Codex 的需求分析原则提炼进 owner docs。
- `docs/PROJECT_GUIDE.md` 的 Q9-Q12 现在更明确要求 run 方向收敛时至少确认：背景与目标、必须做/应该做/可以做、不做项、影响模块、异常流、非功能和验收方式。
- `docs/WORKFLOW.md` 现在把这些内容挂到新主线的 `确定需求方向（run 级）` 和 `多角色 fork / 最小 task 拆解`，没有回迁旧 `orient/choose/council/arbiter` 为正式流程。
- `docs/ENTITIES.md` 现在补了 run/task 的需求边界字段建议，并明确推荐角色是 `run-main/dev/test/arch`，其中 `test` 独立验证、`arch` 按需启用。

## Commands / Outputs (project-guide requirement-analysis principles)
- `python3 tools/taskclient.py --create --title "project-guide requirement-analysis principles" ... --activate` -> pass
- `python3 tools/init.py` -> pass to completion; 仍因脏工作区返回 `INIT_STATUS: needs_fix`
- `python3 tools/appserverclient.py --learnbaseline` -> pass; baseline 已复用
- `python3 tools/appserverclient.py --fork-current` -> pass; 当前 fork thread=`019ce5e2-50f1-7b20-aadf-4b746a1d1467`

## Project guide probing templates
- 新建并完成 `task-project-guide-probing-templates`，继续只增强 `PROJECT_GUIDE` 的学习协议层，不改题库结构。
- 在 Q9-Q12 下补了少量高质量追问模板，帮助 AI 面对杂乱需求材料时，先把 run 方向、角色分工、对象分层和 task 前置边界问清楚。
- 追问模板聚焦：背景与目标、必须做/应该做/可以做、不做项、影响模块、异常流、非功能、验收，以及哪些问题属于 run、task 或 thread summary。

## Project guide self-structuring skeleton
- 新建并完成 `task-project-guide-self-structuring-skeleton`，继续只在 `PROJECT_GUIDE` 里增强 AI 自我学习协议。
- 在 Q9-Q12 下补了最小“自我梳理输出骨架”，让 AI 读完客户杂乱材料后，先产出自己的 `run_goal/scope/non_goals/impacted_modules/risks/acceptance`、`role_plan`、`object_layer`、`task_ready` 等草稿结构。
- 这一步仍然不改题号、不新增独立实现层，只把高质量提问进一步压成可复用的结构化思考骨架。

## Project guide markdown draft template
- 新建并完成 `task-project-guide-markdown-draft-template`，继续只增强协议层，不碰任何运行时或自动化实现。
- 在 `docs/PROJECT_GUIDE.md` 的 Q12 下新增标准化 `Markdown intake draft` 模板，用于 AI 读完客户杂乱材料后的首轮结构化输出；模板覆盖 `Background / Run Goal / Scope / Non-Goals / Impacted Modules / Risks / Non-Functional Constraints / Acceptance / Role Plan / Task Candidates / Open Questions / Summary Target`。
- `docs/WORKFLOW.md` 与 `docs/ENTITIES.md` 同步明确：`Markdown intake draft` 只是 run 级协议层草稿，用于把客户材料先整理成讨论输入，不等于 `run summary`，也不是机器真相源。

## Project bootstrap learning protocol
- 新建并完成 `task-project-bootstrap-learning-protocol`，把“陌生项目尚未接入基座时如何先学习、再补 owner docs、最后再考虑自动化接入”沉淀成独立协议文档 [PROJECT_BOOTSTRAP_PROTOCOL.md](/root/quant-factory-os/docs/PROJECT_BOOTSTRAP_PROTOCOL.md)。
- 该协议明确：面对只有杂乱文档、半截代码、零散认知的新项目，先使用通用 `PROJECT_GUIDE` 题库做首轮学习，再补项目化 `PROJECT_GUIDE/WORKFLOW/ENTITIES/AGENTS`，而不是先复制 `tools/` 或直接开始实现。
- `docs/PROJECT_GUIDE.md`、`docs/WORKFLOW.md`、`docs/FILE_INDEX.md` 已同步引用这份 bootstrap 协议，口径上把“通用学习协议”和“项目化 owner docs”分清。

## Multi-thread collaboration minimum chain
- 新建并完成 `task-multi-thread-collaboration-minimum-chain`，把最小多线程协作链先收敛到 `run-main -> dev/test -> thread summary -> task summary`，不直接跳到完整多 agent orchestration。
- `TASKS/_SCHEMA.task.json` 现在新增 `role_threads` 和 `test_gate`；`role_threads` 固定最小角色位为 `run-main/dev/test/arch`，`test_gate` 承担 task 内独立验证门。
- `tools/taskclient.py` 现已支持：
  - `--role-threads`
  - `--set-role-thread`
  - `--test-gate`
  - `--set-test-gate`
- 真实验证已通过：当前 task 已写入 `dev` 角色线程样例和一个 `blocked` 的 `test_gate`，说明“实现侧”和“独立验证侧”的最小机器层已存在。

## Appserverclient fork role command
- 新建并完成 `task-appserverclient-fork-role-command`，把最小 role thread binding 接到真实 runtime。
- `tools/appserverclient.py` 现在支持 `python3 tools/appserverclient.py --fork-role <dev|test|arch>`：它会基于当前 `fork_current_session` fork 出真实 role thread，命名后回写到当前 task 的 `role_threads.<role>`。
- 真实验证已通过：本轮成功 fork 出 `test` role thread `019ce643-7e04-7d61-a980-bec20518d20b`，并写回 [TASKS/TASK-appserverclient-fork-role-command.json](/root/quant-factory-os/TASKS/TASK-appserverclient-fork-role-command.json)。

## Appserverclient role-turn runtime
- 新建并完成 `task-appserverclient-role-turn-runtime`，把最小 role thread 执行面接到真实 runtime。
- `tools/appserverclient.py` 现在支持 `python3 tools/appserverclient.py --role-turn <dev|test|arch> [text...]`：它会恢复已绑定的 role thread，并在该线程上执行真实 turn。
- 为当前 task 先真实 fork 并绑定了 `test` role thread `019ce64a-8ad1-7733-a6e0-f8b0c15d22f2`，然后成功执行：
  - `python3 tools/appserverclient.py --role-turn test "请用一句话说明你当前作为 test 线程的职责。"`
- 本次真实返回的 `last_agent_message` 为：`我当前作为 test 线程的职责，是基于主线合同独立验证实现是否满足预期、暴露风险与回归缺口，并把可回灌的测试结论沉淀为 run 级证据。`
- 这一步只打通 role thread 的执行面，不做 thread summary 自动回收，也不做多角色调度器。

## Role thread summary to task summary
- 新建并完成 `task-role-thread-summary-to-task-summary`，把 `thread summary -> task summary` 的最小回收链接到真实 runtime。
- `TASKS/_SCHEMA.task.json` 新增 `role_summaries`，`task_summary` 新增 `role_summary_evidence`。
- `tools/appserverclient.py` 新增 `python3 tools/appserverclient.py --summarize-role <role>`，它会恢复已绑定的 role thread、发送 role summary prompt、抽取最后一条 agent message，并写回当前 task 的 `role_summaries.<role>`。
- 同时，task 机器层会追加：
  - `task_summary.source_threads`
  - `task_summary.role_summary_evidence`
- 真实验证已通过：
  - `python3 tools/appserverclient.py --fork-role test`
  - `python3 tools/appserverclient.py --role-turn test "请从独立测试视角给出这个 task 当前最关键的验证关注点。"`
  - `python3 tools/appserverclient.py --summarize-role test`
  - `python3 tools/taskclient.py --role-summaries`
  - `python3 tools/taskclient.py --active-task`

## Task role summary merge rules
- 新建并完成 `task-task-role-summary-merge-rules`，把多角色 role summaries 并存时的 task-level 最小聚合收进 `taskclient`。
- `tools/taskclient.py` 新增 `python3 tools/taskclient.py --merge-role-summaries`。
- 当前聚合规则只做最小去重追加：
  - `task_summary.source_threads`
  - `task_summary.role_summary_evidence`
  - `task_summary.key_updates` 中的 `<role> summary merged`
- 真实验证已通过：
  - `python3 tools/taskclient.py --merge-role-summaries --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
  - `python3 tools/taskclient.py --task-summary --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`

## Task role summary conflict rules
- 新建并完成 `task-task-role-summary-conflict-rules`，把 task 层的最小冲突优先级和缺口汇总规则落到机器层。
- `TASKS/_SCHEMA.task.json` 现在把这两块定义为：
  - `task_summary.conflict_policy`
  - `task_summary.gap_summary`
- `tools/taskclient.py` 新增 `python3 tools/taskclient.py --refresh-task-gaps`，会基于：
  - `role_summaries`
  - `test_gate`
  刷新 `missing_roles` 和 `open_gaps`
- 当前默认优先级顺序是：
  - `run-main -> test -> arch -> dev`
- 真实验证已通过：
  - `python3 tools/taskclient.py --refresh-task-gaps --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
  - `python3 tools/taskclient.py --task-summary --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`

## Run-main role runtime resolution link
- 新建并完成 `task-run-main-role-runtime-resolution-link`，把 `run-main` 的真实 role runtime 与 task resolution 自动刷新串起来。
- `appserverclient --fork-role` 现在正式支持 `run-main`，不再只限 `dev/test/arch`。
- 已真实验证：
  - `python3 tools/appserverclient.py --fork-role run-main`
  - `python3 tools/appserverclient.py --role-turn run-main "..."`
  - `python3 tools/appserverclient.py --summarize-role run-main`
- `summarize-role run-main` 后，task 机器层会自动刷新：
  - `task_summary.gap_summary`
  - `task_summary.escalation_summary`
  - `task_summary.run_main_resolution`
- 本次真实结果中：
  - `role_threads.run-main.thread_id=019ce69a-7e4f-7aa3-b1f2-9e9299c70d61`
  - `role_summaries.run-main.summary_turn_id=019ce69c-2cfa-73a1-a821-25634ddbdc43`
  - `escalation_summary.needs_run_main=true`
  - `run_main_resolution.status=acknowledged`
  - 仍等待 `test_gate=passed` 才能关闭升级项

## Commands / Outputs (run-main role runtime resolution link)
- `python3 -m py_compile tools/appserverclient.py tools/taskclient.py` -> pass
- `python3 tools/appserverclient.py --fork-role run-main` -> pass
- `python3 tools/appserverclient.py --role-turn run-main "请从 run-main 视角确认当前 task 的升级项，并说明关闭升级前还缺什么。"` -> pass
- `python3 tools/appserverclient.py --summarize-role run-main` -> pass; 自动刷新 `gap_summary` / `escalation_summary` / `run_main_resolution`
- `python3 tools/taskclient.py --run-main-resolution --task-json-file TASKS/TASK-run-main-role-runtime-resolution-link.json` -> pass; 当前返回 `status=acknowledged`

## Test role gate runtime link
- 新建并完成 `task-test-role-gate-runtime-link`，把 `test` 真实 role thread、`test_gate` 写回和升级项关闭条件串起来。
- `appserverclient` 现在新增：
  - `--mark-test-gate <pending|blocked|passed> [evidence...]`
- 已真实验证：
  - `python3 tools/appserverclient.py --fork-role test`
  - `python3 tools/appserverclient.py --role-turn test "..."`
  - `python3 tools/appserverclient.py --summarize-role test`
  - `python3 tools/appserverclient.py --mark-test-gate passed "real test gate passed from runtime"`
- 为了把关闭链完整跑通，本轮还在同一 task 下补了：
  - `python3 tools/appserverclient.py --fork-role run-main`
  - `python3 tools/appserverclient.py --summarize-role run-main`
- 当前最终结果：
  - `test_gate.status=passed`
  - `escalation_summary.needs_run_main=false`
  - `run_main_resolution.status=not_needed`
  - `task_summary.role_summary_evidence` 已同时保留 `run-main` 与 `test` 的真实 summary turn 证据

## Commands / Outputs (test role gate runtime link)
- `python3 -m py_compile tools/appserverclient.py tools/taskclient.py` -> pass
- `python3 tools/appserverclient.py --fork-role test` -> pass
- `python3 tools/appserverclient.py --role-turn test "请从独立测试视角说明当前 task 关闭升级项前最关键的验证结论。"` -> pass
- `python3 tools/appserverclient.py --summarize-role test` -> pass
- `python3 tools/appserverclient.py --mark-test-gate passed "real test gate passed from runtime"` -> pass
- `python3 tools/appserverclient.py --fork-role run-main` -> pass
- `python3 tools/appserverclient.py --summarize-role run-main` -> pass
- `python3 tools/taskclient.py --run-main-resolution --task-json-file TASKS/TASK-test-role-gate-runtime-link.json` -> pass; 最终返回 `status=not_needed`

## Task escalation to run-main rules
- 新建并完成 `task-task-escalation-to-run-main-rules`，把“哪些冲突必须升级给 run-main”落到 task 机器层。
- `TASKS/_SCHEMA.task.json` 现在新增：
  - `task_summary.escalation_policy`
  - `task_summary.escalation_summary`
- `tools/taskclient.py` 新增 `python3 tools/taskclient.py --refresh-task-escalation`，会基于：
  - `gap_summary`
  - `test_gate`
  刷新当前是否必须升级给 `run-main`
- 当前最小必须升级条件是：
  - `run-main summary missing`
  - `test_gate` 未通过
  - 仍有 blocking issue
- 真实验证已通过：
  - `python3 tools/taskclient.py --refresh-task-gaps --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
  - `python3 tools/taskclient.py --refresh-task-escalation --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
  - `python3 tools/taskclient.py --task-summary --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`

## Dev role runtime merge link
- 新建并完成 `task-dev-role-runtime-merge-link`，把 `dev` 真实 role thread 接到 runtime，并验证 `summarize-role dev` 后会自动 merge 到当前 task summary。
- 已完成真实链路：
  - `--fork-role dev`
  - `--role-turn dev`
  - `--summarize-role dev`
- 当前 task 真相源已落下：
  - `role_threads.dev.thread_id=019ce6aa-e6cb-7903-9f84-938b3e83238c`
  - `role_summaries.dev.summary_turn_id=019ce6c4-9521-7861-b5f7-4881ea0e2f65`
  - `task_summary.role_summary_evidence` 已包含 `dev:019ce6c4-9521-7861-b5f7-4881ea0e2f65`
  - `task_summary.source_threads` 已包含 `dev:019ce6aa-e6cb-7903-9f84-938b3e83238c`
- 这一步证明 `dev` 侧真实 runtime 已从“线程可绑定”推进到“线程可执行并自动沉淀到 task 机器层”。

## Commands / Outputs (dev role runtime merge link)
- `python3 -m py_compile tools/appserverclient.py tools/taskclient.py` -> pass
- `python3 tools/appserverclient.py --fork-role dev` -> pass
- `python3 tools/appserverclient.py --role-turn dev "请从开发视角说明当前 task 已完成什么、还缺什么。"` -> pass
- `python3 tools/appserverclient.py --summarize-role dev` -> pass; 自动执行 `merge_role_summaries` 并刷新 `gap_summary / escalation_summary / run_main_resolution`

## Integrated multi-role runtime chain
- 新建并完成 `task-integrated-multi-role-runtime-chain`，把 `dev/test/run-main` 三条真实 runtime 链收进同一个 task，并验证 task 机器层能同时保留三角色证据与可解释状态。
- 这轮先真实 fork 三条线程：
  - `dev=019ce6c9-1249-7dd1-973c-bc8919994811`
  - `run-main=019ce6c9-205d-7492-935b-8b47440ad620`
  - `test=019ce6c9-636b-7df0-bab0-104b29799c7d`
- 然后真实执行并回收：
  - `role-turn dev/test/run-main`
  - `summarize-role test/dev/run-main`
  - `mark-test-gate blocked ...`
- 当前 task 真相源结果：
  - `role_summaries` 已同时存在 `dev / test / run-main`
  - `task_summary.role_summary_evidence` 同时保留三角色 summary turn
  - `task_summary.source_threads` 同时保留三角色 thread
  - `test_gate.status=blocked`
  - `gap_summary.open_gaps=["test_gate=blocked"]`
  - `run_main_resolution.status=acknowledged`
- 这一步证明多角色 runtime 主线已经不只是“能各自跑”，而是“能在同一 task 下共同形成可解释的机器状态”。

## Commands / Outputs (integrated multi-role runtime chain)
- `python3 -m py_compile tools/appserverclient.py` -> pass
- `python3 tools/appserverclient.py --fork-role dev` -> pass
- `python3 tools/appserverclient.py --fork-role test` -> pass
- `python3 tools/appserverclient.py --fork-role run-main` -> pass
- `python3 tools/appserverclient.py --role-turn dev "请从开发视角说明当前多角色 task 已完成什么、还缺什么。"` -> pass
- `python3 tools/appserverclient.py --role-turn test "请从独立测试视角说明当前多角色 task 最关键的验证关注点与阻塞。"` -> pass
- `python3 tools/appserverclient.py --role-turn run-main "请从 run-main 视角说明当前多角色 task 的收敛状态，以及关闭前还缺什么。"` -> pass
- `python3 tools/appserverclient.py --summarize-role test` -> pass
- `python3 tools/appserverclient.py --summarize-role dev` -> pass
- `python3 tools/appserverclient.py --summarize-role run-main` -> pass
- `python3 tools/appserverclient.py --mark-test-gate blocked "integrated runtime chain verified but final closure still requires explicit test release"` -> pass

## Task summary to run summary aggregation
- 新建并完成 `task-task-summary-to-run-summary-aggregation`，把已验证完成的 `task-integrated-multi-role-runtime-chain` 提升到 run-level machine summary。
- `tools/evidence.py` 现在新增：
  - `python3 tools/evidence.py --merge-task-summary --run-id <RUN_ID> --task-json-file TASKS/TASK-*.json`
- 这次真实聚合后，`reports/run-2026-03-11-vnext-release-baseline/run_summary.json` 已新增：
  - `source_tasks += task-integrated-multi-role-runtime-chain`
  - `completed_tasks += task-integrated-multi-role-runtime-chain`
  - `key_updates / cross_task_decisions / cross_task_risks / verification_overview / next_run_or_next_tasks` 追加来自该 task summary 的稳定字段
- 当前保持最小策略：只做 append-dedup，不做重语义归并。

## Commands / Outputs (task summary to run summary aggregation)
- `python3 -m py_compile tools/evidence.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --merge-task-summary --task-json-file TASKS/TASK-integrated-multi-role-runtime-chain.json` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary` -> pass

## Task-to-run merge rules
- 新建并完成 `task-task-to-run-summary-merge-rules`，把 `task summary -> run summary` 的字段归并规则显式收成三类：
  - `reconcile_only`
  - `append_dedup`
  - `merge_rewrite`
- `reports/_SCHEMA.run_summary.json` 现在显式包含 `merge_policy`，`tools/evidence.py` 也会在读取/保存 `run_summary.json` 时自动补齐该字段。
- 当前规则表是：
  - `active_tasks` / `completed_tasks` -> `reconcile_only`
  - `source_tasks` / `verification_overview` -> `append_dedup`
  - `key_updates` / `cross_task_decisions` / `cross_task_risks` / `next_run_or_next_tasks` -> `merge_rewrite`
- 当前 `merge_rewrite` 仍是规则化轻归并，不做模型推理；它会先去掉 task 前缀、做最小 humanize，再写成 run-level 列表项。
- 已用当前任务做真实样例验证：样例 `key_update/decision/risk/next_step` 合并进 `run_summary.json` 后，没有再以 `task-task-to-run-summary-merge-rules: ...` 的形式进入语义字段；`verification_overview` 则仍按 `append_dedup` 保留 task 前缀。

## Commands / Outputs (task-to-run merge rules)
- `python3 -m py_compile tools/evidence.py` -> pass
- `python3 tools/taskclient.py --set-task-summary --task-json-file TASKS/TASK-task-to-run-summary-merge-rules.json ...` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --merge-task-summary --task-json-file TASKS/TASK-task-to-run-summary-merge-rules.json` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --reconcile-run-summary` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --compact-run-summary` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary` -> pass; `merge_policy` 已落盘，新增样例条目按规则区分 `merge_rewrite` 和 `append_dedup`

## Run summary legacy prefix cleanup strategy
- 新建并完成 `task-run-summary-legacy-prefix-cleanup-strategy`，把历史 `run_summary` 旧 task 前缀条目的处理策略收成“显式维护动作”，不在普通 merge/reconcile 流程中静默重写。
- `tools/evidence.py` 新增：
  - `python3 tools/evidence.py --run-id <RUN_ID> --normalize-run-summary`
- `run_summary.json` 现在新增：
  - `legacy_cleanup_policy`
  - `legacy_cleanup_last_applied_at`
- 当前策略只清理 `merge_rewrite` 字段：
  - `key_updates`
  - `cross_task_decisions`
  - `cross_task_risks`
  - `next_run_or_next_tasks`
- `verification_overview` 和 `source_tasks` 继续保留 task 级证据粒度，不参与这一步重写。
- 真实验证后，当前 run summary 中历史的 `task-integrated-multi-role-runtime-chain:` 语义前缀已被清掉，而 `verification_overview` 仍保持原有证据前缀。

## Commands / Outputs (run summary legacy prefix cleanup)
- `python3 -m py_compile tools/evidence.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --normalize-run-summary` -> pass; 语义字段旧 task 前缀被清理，`legacy_cleanup_last_applied_at` 已落盘
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary` -> pass; `verification_overview` 保持证据粒度，`baseline_ready_summary` 已按清理后的 run-level 表达重建

## Run summary merge quality
- 新建并完成 `task-run-summary-merge-quality`，把 `merge_rewrite` 从“仅去前缀 + humanize”提升到“少量高频模式的 run-level 归并”。
- 当前已规则化归并的模式包括：
  - 多个 `<role> summary merged` -> `multi-role runtime summaries are now preserved at run level`
  - `test gate=blocked/passed` -> 更稳定的 gate 状态表达
  - `all three real summaries are preserved ...` -> 更短的 multi-role run-level 决策句
- 这次真实重跑 `--normalize-run-summary` 后，当前 `run_summary.json` 已从三条分散的 `test/run-main/dev summary merged` 收成一条 run-level 更新。

## Commands / Outputs (run summary merge quality)
- `python3 -m py_compile tools/evidence.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --normalize-run-summary` -> pass; `key_updates` 已收成 `multi-role runtime summaries are now preserved at run level`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary` -> pass; `cross_task_decisions` 也已改成更短的 multi-role run-level 句子

## Run summary risk merge quality
- 新建并完成 `task-run-summary-risk-merge-quality`，继续只收 `cross_task_risks` 的 run-level 归并质量。
- 当前规则化结果已经把：
  - `test gate=blocked` -> `test gate remains blocked`
- 真实重跑后，当前 `cross_task_risks` 已不再保留原始等号写法，而是转成更稳定的 run-level 风险表达。
- 这一轮没有扩大到通用风险改写，只收高频 gate 风险模式。

## Commands / Outputs (run summary risk merge quality)
- `python3 -m py_compile tools/evidence.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --normalize-run-summary` -> pass; `cross_task_risks` 已出现 `test gate remains blocked`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary` -> pass; risk 语句保持 run-level 表达

## Remove Makefile alias layer
- 新建并完成 `task-remove-makefile-alias-layer`，删除 repo 根目录 `Makefile`，把正式入口进一步收成 Python/pytest 原生命令。
- `AGENTS.md` 与 `README.md` 中原本的：
  - `make evidence`
  - `make verify`
  - `make slice`
  已全部替换为：
  - `python3 tools/evidence.py --run-id <RUN_ID>`
  - `pytest -q`
  - `python3 tools/slice.py --run-id <RUN_ID> --day YYYY-MM-DD --symbols A,B --start HH:MM --end HH:MM`
- 这一步的目标不是改能力，而是删掉一层只做转发的别名入口，降低 repo 理解成本。

## Commands / Outputs (remove Makefile alias layer)
- `python3 -m py_compile tools/project_config.py tools/appserverclient.py tools/evidence.py tools/taskclient.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline` -> pass
- `pytest -q` -> `/bin/bash: pytest: command not found`

## Relocate appserver logs and backup assets
- 新建并完成 `task-relocate-appserver-logs-and-backup-assets`，把顶层 `test_app*.jsonl/.log` 收进 `appserver_log/`，并删除顶层 `log.txt`。
- `tools/backup/` 已整体迁到 `chatlogs/backup/`，正式文档与默认路径已同步改到新位置。
- `tools/appserverclient.py` 的默认 runtime 日志输出现在落到：
  - `appserver_log/test_app.events.jsonl`
  - `appserver_log/test_app.stderr.log`
  - `appserver_log/test_app.learn_init.events.jsonl`
  - `appserver_log/test_app.learn_init.stderr.log`

## Commands / Outputs (relocate appserver logs and backup assets)
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py tools/evidence.py tools/taskclient.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline` -> pass
- `find appserver_log chatlogs/backup -maxdepth 1 -type f | sort` -> pass; 日志与归档资产都已落到新目录

## Cleanup stale tasks and reports artifacts
- 新建并完成 `task-cleanup-stale-tasks-and-reports-artifacts`，删除了：
  - `TASKS/QUEUE.md`
  - sample/demo task: `TASK-bootstrap-sample-task.*`、`TASK-schema-sample-task.*`、`TASK-ux-sample-task.*`
  - 孤立旧 task: `TASK-tools-orchestrator-entry.md`
  - reports 下的 `.ipynb_checkpoints` 残留
- 保留了真实 run evidence 和真实 task JSON/MD；这轮只清掉无正式主线价值的样例、兼容和 checkpoint 垃圾。

## Commands / Outputs (cleanup stale tasks and reports artifacts)
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py tools/evidence.py tools/taskclient.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline` -> pass
- 正式面 grep 已无 `TASKS/QUEUE.md` 命中；剩余命中只在 checkpoint/backup 文档

## Archive stale blueprint and project guide backups
- 新建并完成 `task-archive-stale-blueprint-and-project-guide-backups`，把：
  - `docs/PROJECT_GUIDE_1.0_backup.md`
  - `docs/TOOLS_REFACTOR_BLUEPRINT.md`
  移到 `chatlogs/`。
- 审计结果显示，这两个文件已经不在正式文档引用链里；当前只剩 checkpoint 残留提到它们。

## Commands / Outputs (archive stale blueprint and project guide backups)
- `find chatlogs -maxdepth 1 -type f \( -name 'PROJECT_GUIDE_1.0_backup.md' -o -name 'TOOLS_REFACTOR_BLUEPRINT.md' \) -print` -> pass
- 正式面 grep 不再命中这两个 `docs/` 路径；剩余命中只在 checkpoint 残留

## Docs stale flow noise cleanup
- 新建并完成 `task-docs-stale-flow-noise-cleanup`，把正式 `docs/` 面里仍会误导当前主线的旧流程话术删掉。
- 当前处理包括：
  - `PROJECT_GUIDE.md` 不再把旧阶段脚本当作讨论主线
  - `WORKFLOW.md` 删除历史兼容链路整段，只保留当前正式主线
  - `FILE_INDEX.md` 删除 legacy/compatibility 区，避免把归档资产继续放进正式阅读索引
  - `ENTITIES.md` 去掉旧 `direction/selection/ready contract` 等对象定义，改成 run 方向收敛与 task 规划表达
  - `TOOLS_METHOD_FLOW_MAP.md` 去掉历史兼容链路段落

## Commands / Outputs (docs stale flow noise cleanup)
- `grep -RIn "\bready\b\|orient\|choose\|council\|arbiter\|slice_task\|run_main\|discussion artifacts\|execution contract\|orient_choice" docs/*.md | sort` -> 正式 docs 剩余命中只涉及当前对象名 `run_main_resolution`
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py tools/evidence.py tools/taskclient.py` -> pass
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline` -> pass

## Init standard bootstrap skeleton
- 新建并完成 `task-init-standard-bootstrap-skeleton`，把 `init` 扩成最小标准协议骨架创建入口。
- `init` 现在会自动创建最小目录骨架：
  - `TASKS/`
  - `reports/`
  - `chatlogs/`
  - `appserver_log/`
- `init` 现在会自动创建最小协议文件：
  - `AGENTS.md`
  - `README.md`
  - `todo.md`
  - `docs/PROJECT_GUIDE.md`
  - `docs/WORKFLOW.md`
  - `docs/ENTITIES.md`
  - `docs/FILE_INDEX.md`
  - `docs/PROJECT_BOOTSTRAP_PROTOCOL.md`
  - `docs/TOOLS_METHOD_FLOW_MAP.md`
  - `TASKS/QUEUE.json`
  - `TASKS/_SCHEMA.task.json`
  - `TASKS/_SCHEMA.queue.json`
  - `tools/project_config.template.json`
- `tools/project_config.json` 缺失时，`init` 会先 bootstrap 一份最小配置，再继续预检。
- `docs/TOOLS_METHOD_FLOW_MAP.md` 缺失时创建为空文件，不预写内容，等待后续由原始文档、代码现状和 `PROJECT_GUIDE` 反写。

## Commands / Outputs (init standard bootstrap skeleton)
- `python3 -m py_compile tools/init.py tools/project_config.py` -> pass
- `python3 tools/init.py` -> pass to final summary; current result is `needs_fix` only because worktree is dirty

## Init-project gate and bootstrap state
- 新建并完成 `task-init-project-gate-and-bootstrap-state`，把项目首轮接入门禁正式落到 `project_config` 和 `appserverclient`。
- `tools/project_config.json` 与模板现在都带：
  - `bootstrap_state.is_inited`
  - `initialized_at`
  - `initialized_by`
  - `bootstrap_source`
- 当前规则已经写死：
  - 只有 `is_inited = Y` 才允许 baseline 主线
  - 首轮接入入口统一命名为 `python3 tools/appserverclient.py --init-project`
  - `--init-project` 只允许在 `is_inited` 不是 `Y` 且 owner docs 全为空时进入下一步
  - 只要任一 owner doc 非空，就直接报错，避免误覆盖 `PROJECT_GUIDE` 等关键文件

## Commands / Outputs (init-project gate and bootstrap state)
- `python3 -m py_compile tools/project_config.py tools/appserverclient.py tools/init.py` -> pass
- `python3 tools/appserverclient.py --init-project` -> pass as expected on initialized project; returns `project is already initialized`
- 临时将 `bootstrap_state.is_inited` 设为 `N` 后执行 `python3 tools/appserverclient.py --init-project` -> pass as expected; returns `owner docs are not empty`
- `python3 tools/appserverclient.py --learnbaseline` -> pass on current initialized project

## Init-project phase protocol
- 新建并完成 `task-formalize-init-project-phase-protocol`，把 `--init-project` 的两阶段协议正式写进 prompt 和 owner docs。
- 现在的正式约定是：
  - Phase 1: JSON-first 的 plan/gating，先输出 `project_understanding / explicit_refs / light_repo_findings / implementation_gaps / must_read_next / can_write_owner_docs / why_not_ready`
  - Phase 2: Markdown-first 的 owner-doc writing，按目标文件分别生成 `AGENTS.md / PROJECT_GUIDE.md / WORKFLOW.md / ENTITIES.md / FILE_INDEX.md / TOOLS_METHOD_FLOW_MAP.md`
- `session_registry.init_project_session` 现在被明确为初始化过程的独立 session 槽位；默认 `--init-project` 应续跑该 session，只有 `--init-project -new` 才允许重开。
- 默认 intake 规则也已收紧为：先读项目根目录 `README.md`，再读 `docs/**/*.md|txt|doc|docx` 原始材料，同时排除 owner docs 目标文件，避免把反写目标再次当原始材料读回去。

## Commands / Outputs (init-project phase protocol)
- `python3 -m py_compile tools/project_config.py tools/appserverclient.py` -> pass
- `python3 tools/project_config.py` -> pass; 当前 active task 绑定到 `task-formalize-init-project-phase-protocol`，并已收成 `completed`

## Init-project phase-1 intake implementation
- 新建并完成 `task-implement-init-project-phase-1-intake`，把 `--init-project` 从纯预检推进到了最小可运行的 Phase 1 intake。
- 当前 `appserverclient --init-project` 已支持：
  - 默认读取 `README.md` 与 `docs/**/*.md|txt|doc|docx`
  - 排除 owner docs 目标文件
  - 生成 `light_repo_findings`
  - 通过文档显式文件名与真实文件清单做硬匹配
  - 输出第一批 `must_read_next`
- 当前实现仍然只停在 phase-1 gating：
  - 还没有接入真实 `init_project_session` app-server thread
  - 也还没有 owner-doc reverse-writing

## Commands / Outputs (init-project phase-1 intake)
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py` -> pass
- phase-1 smoke test with a temporary demo project root under the repository -> pass; payload now returns `explicit_refs`, `light_repo_findings`, `must_read_next`, and `can_write_owner_docs=false`

## Init-project session resume semantics
- 新建并完成 `task-wire-init-project-session-resume-semantics`，把 `init_project_session` 的最小续跑语义接到了 phase-1 intake。
- 当前行为已经明确：
  - 默认 `python3 tools/appserverclient.py --init-project` 会复用同一个本地 phase-1 session 记录
  - `python3 tools/appserverclient.py --init-project -new` 会显式生成新的 session id
- 同时，owner-doc emptiness 检查和 intake 扫描现在都基于当前 `project_config.required.project_root`，不再绑死 foundation repo 根目录。

## Commands / Outputs (init-project session resume semantics)
- `python3 -m py_compile tools/project_config.py tools/appserverclient.py` -> pass
- local resume/new smoke test on a temporary demo project root -> pass; first and second calls reused the same `init_project_session.thread_id`, and `-new` produced a different id

## Init-project phase-2 writer
- 新建并完成 `task-implement-init-project-phase-2-writer`，把 `--init-project` 的最小 Phase 2 本地写入链接到了 `appserverclient`。
- 当前 `python3 tools/appserverclient.py --init-project --phase2-json <payload.json>` 已支持：
  - 校验 `phase2_write_owner_docs` JSON payload
  - 要求 `write_ready=true`
  - 要求 6 份 owner docs markdown 字段全部非空
  - 只在 owner docs 全为空、`init_project_session.can_write_owner_docs=true` 时写入
  - 全部写入成功后，才把 `bootstrap_state.is_inited` 置为 `Y`
- 当前实现仍然刻意保持最小：
  - 还没有接 app-server init thread
  - 还没有接模型生成 phase-2 payload
  - 但本地 phase-2 write path 已经成立

## Commands / Outputs (init-project phase-2 writer)
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py` -> pass
- temporary demo project smoke test -> pass; `run_init_project(phase2_json=<payload>)` 写入了 `AGENTS.md / docs/PROJECT_GUIDE.md / docs/WORKFLOW.md / docs/ENTITIES.md / docs/FILE_INDEX.md / docs/TOOLS_METHOD_FLOW_MAP.md`，并把 `bootstrap_state.is_inited` 从非 `Y` 切到 `Y`

## Real phase-1 run on a9quant-strategy
- 新建并完成 `task-run-init-project-phase-1-on-a9quant-strategy`，把当前 `init -> --init-project` 主线真实跑到 `/root/a9quant-strategy` 上做验证。
- 这轮先暴露并修掉了两个 bootstrap 问题：
  - `project_config.py` 在目标项目缺少 `docs/PROJECT_GUIDE.md` 时不再直接崩
  - `init` 在未初始化项目上创建的 owner docs 改为空文件，避免和 `--init-project` 的空文件门禁互相冲突
- 修完后，`--init-project` Phase 1 对 `/root/a9quant-strategy` 已能稳定输出：
  - `light_repo_findings`
  - `explicit_refs`
  - `must_read_next`
  - `can_write_owner_docs=false`
  - `why_not_ready=["must_read_next is not empty"]`
- 当前第一批 `must_read_next` 为：
  - `ccxt_utils.py`
  - `advanced_risk.py`
  - `trend_engine.py`
  - `shark_engine.py`
  - `base_bitget_ws.py`
  - `bitget_ws_bridge.py`
  - `market_data_hub.py`
  - `tiny_oms.py`
- 这说明第一轮“README + docs + 轻探测 + 硬匹配”的 intake 机制已经能在真实外部项目上工作，但也暴露出下一步该收的点：当前会把 `docs/.ipynb_checkpoints` 一起扫进去，存在明显噪音。

## Checkpoint noise cleanup for init-project intake
- 新建并完成 `task-exclude-checkpoint-noise-from-init-project-intake`，把 `docs/.ipynb_checkpoints` 纳入 `--init-project` 的扫描排除。
- 现在 `discover_docs_files()` 与 Phase 1 的 `raw_docs_read/docs_files` 都不再包含 checkpoint 噪音目录。
- 重新对 `/root/a9quant-strategy` 跑 Phase 1 后：
  - `raw_docs_read` 已收成 5 份真实原始 docs
  - `docs_files` 也只保留真实材料
  - `must_read_next` 仍保持稳定，不受 checkpoint 噪音干扰

## a9quant-strategy second-round code reads
- 新建并完成 `task-second-round-code-reads-for-a9quant-strategy`，对 phase-1 选出的 8 个 `must_read_next` 文件补了第二轮实现证据读取。
- `advanced_risk.py` 已确认不是占位文件，而是中心化风险层：实现了持久化锚定本金、水位线重置、系统模式状态机（`NORMAL/DEFENSIVE/FROZEN/REBUILD`）和统一 `approve_action` 闸门。
- `ccxt_utils.py` 已确认是具体交易适配层：实现了 `ExchangeTrader` 的市场细节提取、配置校验、保证金/杠杆设置、持仓风控查询、Bitget 专属平仓路径和合约余额查询。
- 结合前一轮已读的 `trend_engine.py`、`shark_engine.py`、`base_bitget_ws.py`、`bitget_ws_bridge.py`、`market_data_hub.py` 和 `tiny_oms.py`，`/root/a9quant-strategy` 当前更像“已有真实交易系统骨架”，而不是只停留在愿景和设计文档阶段。
- 这一轮的结论是：还不能直接进 Phase 2 owner-doc reverse-writing；在反写前仍需补读 `main_controller.py`、`account_state.py`、`contracts.py` 和高价值测试文件，确认真实主入口、状态账本、契约层和验证面。

## Commands / Outputs (a9quant-strategy second-round code reads)
- `python3 tools/project_config.py` -> pass; active task confirmed as `task-second-round-code-reads-for-a9quant-strategy`
- second-round evidence reads completed for:
  - `/root/a9quant-strategy/advanced_risk.py`
  - `/root/a9quant-strategy/ccxt_utils.py`
- previous phase-1 follow-up evidence reused from already read files:
  - `/root/a9quant-strategy/trend_engine.py`
  - `/root/a9quant-strategy/shark_engine.py`
  - `/root/a9quant-strategy/base_bitget_ws.py`
  - `/root/a9quant-strategy/bitget_ws_bridge.py`
  - `/root/a9quant-strategy/market_data_hub.py`
  - `/root/a9quant-strategy/tiny_oms.py`

## a9quant-strategy mainline and test-surface reads
- 新建并完成 `task-read-mainline-state-contracts-and-tests-for-a9quant-strategy`，继续补读 `main_controller.py`、`account_state.py`、`contracts.py`、`test_integration.py` 和 `test_regression.py`。
- `main_controller.py` 已确认真实主入口：`ExchangeTrader -> DataSynchronizer -> AccountState -> RiskManager -> MarketDataHub -> TinyOMS -> BitgetWSBridge -> TrendEngine/SharkEngine` 已在一个异步主控制器中完成编排。
- `account_state.py` 已确认状态账本不是概念层，它把 `DataSynchronizer` 原始快照清洗成 `Position/Account`，再派生 `RiskSnapshot` 和 `StrategySnapshot` 给风控和策略层使用。
- `contracts.py` 已确认项目已有清晰 dataclass 契约层，覆盖 `RiskRequest / TradeIntent / MarketData / StrategyContext / DataSnapshot / Position / Account`。
- `test_integration.py` 与 `test_regression.py` 已确认验证面真实存在，覆盖 live gate、trace propagation、synchronizer-only state update、OMS idempotency、WS reconnect calibration、replay-driven chain 和 risk gate enforcement。
- 这轮之后，`/root/a9quant-strategy` 的真实主线已经足够清楚：它不是只有模块散点，而是已有 controller-centered trading runtime；接下来真正还缺的是 `data_synchronizer.py` 与 `config.json` 的最后一轮依赖/配置证据。

## Commands / Outputs (a9quant-strategy mainline and test-surface reads)
- external code reads completed for:
  - `/root/a9quant-strategy/main_controller.py`
  - `/root/a9quant-strategy/account_state.py`
  - `/root/a9quant-strategy/contracts.py`
  - `/root/a9quant-strategy/test_integration.py`
  - `/root/a9quant-strategy/test_regression.py`

## a9quant-strategy synchronizer and config reads
- 新建并完成 `task-read-synchronizer-and-config-for-a9quant-strategy`，补了最后一轮依赖和配置证据：`data_synchronizer.py` 与 `config.json`。
- `data_synchronizer.py` 已确认同步层采用 `WS 推送为主、REST 定时/事件校准为辅` 的 source-of-truth 模式，已经实现：
  - position/account 原始状态维护
  - `position_uncertain`
  - reconnect / heartbeat 健康信号
  - `force_rest_sync`
  - `get_consistency_score`
  - `is_private_ready`
  - execution-event evidence hooks
- `config.json` 已确认当前运行假设是：
  - Bitget
  - sandbox=true
  - proxy enabled
  - swap
  - `BTC/USDT:USDT`
  - `initial_capital=200`
- 到这一步，`/root/a9quant-strategy` 的 controller、同步层、状态账本、契约层、风控层、执行层、ws 桥接和测试面都已有证据，不再只是局部模块采样。
- 当前剩余判断已经不是“证据够不够写 owner docs”，而是“是否现在就进入 Phase 2，以及如何在反写时显式保留 sample config 的 sandbox-credential hygiene 风险”。

## Commands / Outputs (a9quant-strategy synchronizer and config reads)
- external reads completed for:
  - `/root/a9quant-strategy/data_synchronizer.py`
  - `/root/a9quant-strategy/config.json`

## a9quant-strategy phase-2 draft payload
- 新建并完成 `task-prepare-a9quant-strategy-phase-2-draft-payload`，基于已完成的 phase-1 证据，生成了一版**只供审阅、不执行写入**的 phase-2 payload 草稿。
- 草稿路径是：
  - `learn/a9quant-strategy_phase2_draft.json`
- 这版 payload 已包含：
  - `phase = phase2_write_owner_docs`
  - `write_ready = true`
  - `agents_md`
  - `project_guide_md`
  - `workflow_md`
  - `entities_md`
  - `file_index_md`
  - `tools_method_flow_map_md`
  - `remaining_unknowns`
- 当前策略仍保持克制：
  - 已生成可执行格式的 payload
  - 但尚未对 `/root/a9quant-strategy` 运行 `--init-project --phase2-json`
- 草稿内容继续保留了真实风险，而不是把目标项目描述成已经完全清洁和完全抽象化的系统：
  - sandbox credentials / proxy defaults
  - Bitget-specific coupling
  - static-inspection-only review boundary

## Commands / Outputs (a9quant-strategy phase-2 draft payload)
- generated:
  - `learn/a9quant-strategy_phase2_draft.json`

## init-project session-first simplification
- 新建并完成 `task-simplify-init-project-to-session-first-flow`，把 `--init-project` 从“半程序推理 + phase2 写入”收回到通用的 session-first 初始化流程。
- 这轮正式删掉了 `appserverclient.py` 里针对具体项目语义的 question heuristics，Phase 1 不再靠硬编码领域词去回答 `Q1/Q2/Q3/Q5/Q6/Q11`。
- 这轮也删掉了旧的 `--phase2-json` 路径，正式面只保留：
  - `python3 tools/appserverclient.py --init-project`
  - `python3 tools/appserverclient.py --update-init-project --payload-json <path>`
  - `python3 tools/appserverclient.py --complete-init-project`
- 当前 `--init-project` 的正式职责已经收成：
  - 保持 `bootstrap_state` 与 `init_project_session`
  - 以 `xhigh plan` 和通用提示词模板推进 17 问理解
  - 返回 `answered_questions / unclear_questions / customer_followups / document_priority_understanding / current_project_understanding / ready_for_doc_write`
  - 在同一 session 上继续人工纠偏与状态推进
- 这轮没有再扩新的 heuristic，也没有继续把 owner-doc 自动写入塞回 runtime。

## Commands / Outputs (init-project simplification)
- verified:
  - `python3 -m py_compile tools/appserverclient.py tools/project_config.py tools/init.py`
  - `python3 tools/project_config.py`

## init-project session instruction and update schema
- 新建并完成 `task-extend-init-project-session-instruction-and-update-schema`，把“一句话高质量执行指令”正式接进 `--init-project`。
- 当前新增的正式入口是：
  - `python3 tools/appserverclient.py --init-project --instruction-text "<一句补充执行指令>"`
  - `python3 tools/appserverclient.py --init-project --instruction-file docs/xxx.md`
- 当前 `init_project_session` 现在会持久化：
  - `session_execution_instruction`
  - `operator_notes`
- 这意味着：
  - 你可以先用一句高质量说明定义当前 init session 的阅读顺序、文档优先级和 owner 关注点
  - 再在同一个 session 上继续手工纠偏
  - 然后通过 `--update-init-project --payload-json <path>` 把最新理解和备注写回状态

## Commands / Outputs (init-project session instruction)
- verified:
  - `python3 -m py_compile tools/appserverclient.py tools/project_config.py tools/init.py`
  - `python3 tools/appserverclient.py --init-project --instruction-text "总纲优先，README 次之，中央银行设计是风控与现金流核心"`
  - current repo correctly remained blocked by `is_inited = Y`, which confirms the new CLI path is wired into the formal gate

## init-project instruction flow on uninitialized fixture
- 新建并完成 `task-validate-init-project-instruction-flow-on-uninitialized-fixture`，对仓库内未初始化 fixture 真实跑通：
  - `python3 tools/init.py`
  - `python3 tools/appserverclient.py --init-project -new --instruction-text "总纲优先，README 次之，中央银行设计是风控与现金流核心"`
- 这轮确认了两件真正关键的事：
  - `session_execution_instruction` 已进入 `err_code=1012` 的返回 payload
  - 更重要的是，它已真实落到目标项目自己的 `fixtures/init_project_fixture/tools/project_config.json -> session_registry.init_project_session`
- 同时也确认：
  - 当前 `--init-project` 仍保持 fail-closed
  - `ready_for_doc_write=false`
  - `customer_followups` 会先提示“按本轮补充执行指令校正文档优先级、阅读顺序和 owner 关注点”
- 这说明当前 init-project 已经具备你要的最小手工续跑形态：先打一轮、再进同一 session 继续纠偏和补料、再 update/complete。

## Commands / Outputs (fixture instruction flow)
- verified:
  - `python3 tools/init.py`
  - `python3 tools/appserverclient.py --init-project -new --instruction-text "总纲优先，README 次之，中央银行设计是风控与现金流核心"`
  - `python3 tools/view.sh fixtures/init_project_fixture/tools/project_config.json --from 1 --to 160`

## init-project p-only prompt semantics
- 新建并完成 `task-init-project-p-only-prompt-semantics`，把 `--init-project` 的 CLI 语义再收紧一层：
  - `-p` 现在是唯一的完整 prompt 开关
  - `-new` 只负责重开 init thread，不再隐式等于 prompt 模式
  - 无 init thread 时，`--init-project -t "..."` 会新建真实 thread，但只发送聊天文本，不自动重喂完整 prompt
- 这次改动的目的不是扩功能，而是把 `init-project` 的参数行为收成产品直觉：线程创建和完整 prompt 注入是两件不同的事，不再绑定。

## Commands / Outputs (p-only prompt semantics)
- verified:
  - `python3 -m py_compile tools/appserverclient.py tools/project_config.py`
  - `python3 -m py_compile /root/a9quant-strategy/tools/appserverclient.py /root/a9quant-strategy/tools/project_config.py`
  - lightweight monkeypatch branch check:
    - `force_new + -t` -> `created_real_init_thread_chat_turn`
    - `force_new + -p + -t` -> `created_real_init_thread`

## fix init-project chat turn plan xhigh
- 新建并完成 `task-fix-init-project-chat-turn-plan-xhigh`，修复了非 prompt 的 init-project chat turn 掉回 `default + low` 的问题。
- 现在即使只执行 `--init-project -new -t "你好"`，底层也会沿 init-thread 的运行时壳走：
  - `mode = plan`
  - `effort = xhigh`
- 这次没有再改输出 payload 形状，只修正运行时壳，避免继续把问题面扩大。

## Commands / Outputs (chat turn plan+xhigh fix)
- verified:
  - `python3 -m py_compile tools/appserverclient.py tools/project_config.py`
  - `python3 -m py_compile /root/a9quant-strategy/tools/appserverclient.py /root/a9quant-strategy/tools/project_config.py`
  - monkeypatch runtime check:
    - `continue_init_project_chat_turn(..., create_new_thread=True)` now constructs `CodexAppClient(mode='plan', effort='xhigh')`
## 2026-03-18 - manual rewrite a9quant owner docs from source hierarchy

- 这轮不走 init-project 自动化，不看 phase1 JSON，直接以 `/root/a9quant-strategy` 的原始文档和关键实现为依据，手工重写 7 份 owner docs。
- 固定优先级已落到目标项目文档：
  - `docs/总纲清单（可复制）.md`
  - `README.md`
  - `docs/中央银行设计.md`
  - `docs/基于资管双向非对称对冲策略手册.md`
  - `docs/梦想中的交易资管财富系统想法.md`
  - `docs/资管双向原始想法.md`
- `/root/a9quant-strategy/docs/PROJECT_GUIDE.md` 已重写为 17 问课程文档，不再是摘要页；当前把“三账本财富系统、中央银行闸门、一期开局 B 类、先文档后代码”收成了明确标准答案。
- 同步重写的还有：
  - `/root/a9quant-strategy/AGENTS.md`
  - `/root/a9quant-strategy/docs/WORKFLOW.md`
  - `/root/a9quant-strategy/docs/ENTITIES.md`
  - `/root/a9quant-strategy/docs/FILE_INDEX.md`
  - `/root/a9quant-strategy/docs/TOOLS_METHOD_FLOW_MAP.md`
  - `/root/a9quant-strategy/docs/PROJECT_BOOTSTRAP_PROTOCOL.md`
- 最小校验已完成：上述 7 个文件均已从 0 字节变为非空，`PROJECT_GUIDE.md` 首段显式写出固定阅读顺序。

## 2026-03-18 - debug a9quant learnbaseline PROJECT_GUIDE parsing compatibility

- 真实执行 `/root/a9quant-strategy` 的 `python3 tools/appserverclient.py --learnbaseline -new` 后，定位到问题不在 a9 的 `PROJECT_GUIDE.md`，而在 foundation 侧 `learnbaseline` 对 `必查文件` 的旧解析假设。
- foundation 与 `/root/a9quant-strategy` 的 `tools/project_config.py` 已同步修复：`parse_project_guide_prompt_inputs()` 现在只提取真实 repo 内文件路径，自动忽略 `同上`、`foundation 仓 ...`、`本项目 7 份 owner docs` 等说明性条目。
- 直接构建 `/root/a9quant-strategy` 的 baseline prompt 后，`Additional required files to read with tools/view.sh` 已收敛为真实文件列表，不再混入说明性 bullet。
- 继续沿真实 rollout 排查后，又定位到 `tools/appserverclient.py` 的 `start_turn()` 把 `sandboxPolicy` 写死成了 `readOnly`；这会覆盖 thread/start 的 `workspaceWrite` 能力，放大 app-server 里的 `bwrap/namespace` 问题。
- foundation 与 `/root/a9quant-strategy` 的 `tools/appserverclient.py` 已同步修复：`turn/start` 现在显式发送 `sandboxPolicy = workspaceWrite`。

## a9quant-strategy business-first sync docs refinement
- 本轮没有再碰 runtime 或自动化，只继续收 a9 的同频文档。
- 已新增 `/root/a9quant-strategy/docs/FOUNDATION_BRIDGE.md`，把 foundation 收口成单独的工程承接说明：
  - 它是什么
  - 它有什么用
  - 为什么与 Codex 并用
  - 它和项目的关系
  - 常用命令与两阶段开发模式
- 已更新 `/root/a9quant-strategy/docs/PROJECT_GUIDE.md`：
  - 新增“与 foundation 的关系”短节
  - foundation 不再作为业务逻辑主要解释源
  - 核心题继续以业务为中心，只在需要工程承接时引到 `docs/FOUNDATION_BRIDGE.md`
- 已更新 `/root/a9quant-strategy/docs/总纲清单（可复制）.md`：
  - 在不可变研发闭环后新增一期/二期分期澄清
  - 明确二期 lab 更偏 `AI策略创作 -> backtesting/极限电池 -> replay仿真一致性`
  - 明确一期现实主线是中央银行总控下的确定性策略试点、模拟盘/实盘接通、问题分析与执行数据反哺优化
- 已最小更新 `/root/a9quant-strategy/docs/PROJECT_BOOTSTRAP_PROTOCOL.md` 与 `/root/a9quant-strategy/docs/FILE_INDEX.md`，把 `docs/FOUNDATION_BRIDGE.md` 纳入工程承接说明，但不放进首轮业务阅读顺序。
- 当前同频口径已收成：
  - 业务真相以总纲、README、中央银行设计、策略手册为主
  - foundation 只是一份工程桥接说明，不再压过业务主线

## foundation embedding + queue denoise
- 当前基座已经开始把代码与同频流程嵌入外部业务项目中验证，这说明主线不再只是仓内自转，而是已经进入真实项目接入阶段。
- 为避免新 session 继续被旧的 a9 文档修复上下文污染，本轮已把 active task 切到新的 cleanup task。
- `TASKS/QUEUE.json` 已去掉 completed 项，只保留 active/pending/open 队列项，让当前主线视图回到干净状态。
- `docs/WORKFLOW.md` 和 `docs/PROJECT_GUIDE.md` 只做了最小口径更新：明确 foundation 已开始嵌入外部业务项目验证，因此本仓主线文档要继续保持业务无关、流程优先。

## task files hard cleanup
- 本轮按要求直接删除了 `TASKS/` 下除当前 cleanup task 之外的旧 task 文件。
- 共清理 237 个历史 task JSON/MD 文件；当前 `TASKS/` 只保留：
  - `TASK-session-denoise-and-mainline-cleanup.json`
  - `TASK-session-denoise-and-mainline-cleanup.md`
- 这样新 session 不会再被旧 task 噪音污染，当前主线只剩一个 task 指针和一个 queue 项。

## old reports cleanup
- 本轮继续清理 `reports/` 噪音，删除了两个旧的非当前 run 目录：
  - `run-2026-03-08-remove-templates-pivot`
  - `run-2026-03-08-tools-orchestrator-entry`
- 当前 `reports/` 只保留：
  - 当前主线 run `run-2026-03-11-vnext-release-baseline`
  - `projects/`
  - `_SCHEMA.run_summary.json`
  - `.gitkeep`

## tools experimental line init / sync refresh
- 本轮把 [tools/init.py](/root/quant-factory-os/tools/init.py) 升级成当前实验线准备层入口，不再沿用旧 `RuntimeState / bootstrap_state` 叙事。
- 新的 `tools/init.py` 当前会：
  - 补齐并校验 [tools/project_config.template.json](/root/quant-factory-os/tools/project_config.template.json) 与 [tools/project_config.json](/root/quant-factory-os/tools/project_config.json)
  - 检查 docs、TASKS、state、reports、artifacts、logs、appserver_log、`.agents/skills`、schemas、tests
  - 输出 `INIT_STEP[...]`
  - 输出 `APP_RUNTIME_STATE_START/END`
  - 检查 `codex`、`app-server` 与 git 工作区
- 真实验证已完成：
  - `python3 tools/init.py`
  - 返回 `needs_fix`
  - 原因是 `WORKTREE_DIRTY`
  - 说明脚本已正常运行，当前只是工作区脏
- 本轮新增 [tools/project_config.template.json](/root/quant-factory-os/tools/project_config.template.json)，作为新实验线最小配置模板。
- 本轮同时更新了 [tools/sync_tools.py](/root/quant-factory-os/tools/sync_tools.py)：
  - 同步清单切到新的 runtime bundle
  - 当前会同步 docs、schemas、skills、`tools/app.py`、`tools/main.py`、`tools/init.py`、`tools/project_config.template.json` 和 tests
  - 默认不覆盖目标项目自己的 `tools/project_config.json`
  - 已支持目录级复制
- 真实验证已完成：
  - `python3 tools/sync_tools.py --dry-run`
  - 当前默认目标 `/root/a9quant-strategy` 可正确列出待同步文件
- 主线文档也同步更新：
  - [AGENTS.md](/root/quant-factory-os/AGENTS.md)
  - [docs/WORKFLOW.md](/root/quant-factory-os/docs/WORKFLOW.md)
  - [docs/FILE_INDEX.md](/root/quant-factory-os/docs/FILE_INDEX.md)
