# A9 Quant Strategy Fixture

这个 fixture 用于验证 `python3 tools/appserverclient.py --init-project` 在更接近真实项目材料层级时，是否仍能稳定给出首轮 17 问理解结果。

阅读优先级：
- `docs/总纲清单（可复制）.md`
- `docs/中央银行设计.md`
- `docs/基于资管双向非对称对冲策略手册.md`
- `docs/梦想中的交易资管财富系统想法.md`
- `docs/资管双向原始想法.md`

当前理解约束：
- 总纲清单是总纲宪法，先回答整个系统最终想成为什么。
- README 是项目入口说明，负责告诉 AI 先看什么、当前做到哪里。
- 中央银行设计是亮点特色，也是风控和现金流治理核心。
- 策略手册描述第一期具体实现策略，不等于整个系统终局。
- 另外两份文档是原始想法来源，帮助理解愿景演化，但优先级低于总纲和中央银行设计。

当前实现线索：
- `main_controller.py` 是组合根和真实主入口。
- `data_synchronizer.py` 维护原始状态真相源。
- `advanced_risk.py` 是风险闸门与制度约束中心。
- `contracts.py` 提供 typed contracts。
- `tiny_oms.py` 是统一执行边界。

当前 owner docs 还没有正式反写完成，需要先用 17 问理解项目，再决定是否可以继续写文档。
