from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_task_codex_denylist_exists() -> None:
    denylist = REPO_ROOT / ".codex_read_denylist"
    assert denylist.exists(), ".codex_read_denylist is missing"
    text = denylist.read_text(encoding="utf-8")
    assert "project_all_files.txt" in text


def test_task_codex_view_tool_exists() -> None:
    view_tool = REPO_ROOT / "tools" / "view.sh"
    assert view_tool.exists(), "tools/view.sh is missing"

