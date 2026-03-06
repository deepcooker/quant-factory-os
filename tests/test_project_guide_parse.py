from __future__ import annotations

from pathlib import Path

import pytest

from tools.learn import parse_project_guide



def test_parse_project_guide_extracts_questions(tmp_path: Path) -> None:
    guide = tmp_path / "PROJECT_GUIDE.md"
    guide.write_text(
        """# PROJECT_GUIDE.md

## 一句话北极星
自动化 -> 自我迭代 -> 涌现智能。

### Q1. 项目是什么
#### 为什么问这题
确认主线。
#### 标准答案
这是项目说明。
#### 必查文件
- AGENTS.md
- docs/WORKFLOW.md
#### 查找线索
- 先看 AGENTS
#### 主线意义
- 防止跑偏

### Q2. 当前状态是什么
#### 为什么问这题
确认上下文。
#### 标准答案
这是状态说明。
#### 必查文件
- TASKS/STATE.md
- reports/<RUN_ID>/summary.md
#### 查找线索
- 先看 STATE
#### 主线意义
- 锁定当前执行面
""",
        encoding="utf-8",
    )

    north_star, questions = parse_project_guide(guide, "project-0", "run-1")
    assert north_star == "自动化 -> 自我迭代 -> 涌现智能。"
    assert [q.question_id for q in questions] == ["Q1", "Q2"]
    assert questions[1].must_read_files == ["TASKS/STATE.md", "reports/run-1/summary.md"]



def test_parse_project_guide_requires_sections(tmp_path: Path) -> None:
    guide = tmp_path / "PROJECT_GUIDE.md"
    guide.write_text(
        """# PROJECT_GUIDE.md

### Q1. 项目是什么
#### 为什么问这题
确认主线。
#### 标准答案
这是项目说明。
#### 必查文件
- AGENTS.md
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="missing section"):
        parse_project_guide(guide, "project-0", "")
