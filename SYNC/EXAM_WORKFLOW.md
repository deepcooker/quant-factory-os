# 同频考试工作流（CLI + 网页 GPT）

目标：用“结构化学习 + 自动评分”保证思想层同频，不靠主观感觉。

## 1) 让模型进入考试模式
- Codex CLI：使用 `/plan`，粘贴 `SYNC/EXAM_PLAN_PROMPT.md` 内容。
- 网页 GPT：直接粘贴 `SYNC/EXAM_PLAN_PROMPT.md` 内容。

## 2) 固定答题模板
- 模板：`SYNC/EXAM_ANSWER_TEMPLATE.md`
- 输出文件：`reports/<RUN_ID>/onboard_answer.md`

## 3) 机器评分（CLI）
```bash
/root/policy/venv/bin/python tools/sync_exam.py \
  --answer-file reports/<RUN_ID>/onboard_answer.md \
  --rubric-file SYNC/EXAM_RUBRIC.json \
  --output-file reports/<RUN_ID>/sync_exam_result.json \
  --run-id <RUN_ID>
```

## 4) 通过标准
- 分数 >= 80
- 必填项（required checks）全部通过
- 输出包含：
  - `SYNC_EXAM_PASS: true`
  - `SYNC_EXAM_SCORE: <score>`

## 5) 不通过处理
- 优先修正 failed checks，不允许跳过评分直接执行任务。
- 修正后重新评分，直到通过。
