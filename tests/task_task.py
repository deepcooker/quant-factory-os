from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_task_task_script_exists() -> None:
    task_tool = REPO_ROOT / "tools" / "task.sh"
    assert task_tool.exists(), "tools/task.sh is missing"


def test_task_task_mentions_queue_contract() -> None:
    text = (REPO_ROOT / "tools" / "task.sh").read_text(encoding="utf-8")
    assert "TASKS/QUEUE.md" in text
    assert "TASKS/STATE.md" in text

