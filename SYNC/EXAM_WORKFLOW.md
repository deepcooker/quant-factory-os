# 同频考试工作流（v2）

目标：用统一深度问卷验证“真正同频”，并保留可审计证据。

## 1) 进入考试模式
- 使用题面：`SYNC/EXAM_PLAN_PROMPT.md`
- 答题模板：`SYNC/EXAM_ANSWER_TEMPLATE.md`

## 2) 产出答卷
- 输出路径：`reports/<RUN_ID>/onboard_answer.md`
- 要求：每个问题必须写证据路径；推理必须写依据。

## 3) 机器评分
```bash
tools/qf exam-auto RUN_ID=<RUN_ID>
```
或
```bash
tools/qf exam RUN_ID=<RUN_ID>
```

## 4) 通过标准
- 分数 >= 85
- required checks 全通过
- 输出包含：
  - `SYNC_EXAM_PASS: true`
  - `SYNC_EXAM_SCORE: <score>`

## 5) 不通过处理
- 先修 failed checks 指向的问题。
- 重新评分，直到通过。
- 不允许跳过考试直接进入执行。
