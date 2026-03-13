# TODO

- 将 `Markdown intake draft` 抽成独立可复用模板文件，方便后续跨项目实验直接使用。
- 继续收敛“陌生项目首轮学习 -> 项目化 owner docs 补齐”的最小输出清单。
- 等当前基座协议稳定后，再评估是否对 `/root/a9quant-strategy` 做真实 bootstrap 实验。
- 等四个主工具边界稳定后，再评估 `agent` 角色配置化：
  - 角色定义放配置
  - 角色提示词放模板
  - runtime 只负责 `fork/turn/summarize`
  - 不把角色逻辑继续硬编码进 `appserverclient`
