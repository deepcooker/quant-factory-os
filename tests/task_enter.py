from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_task_enter_wrapper_files_exist() -> None:
    enter = REPO_ROOT / "tools" / "enter.sh"
    onboard = REPO_ROOT / "tools" / "onboard.sh"
    assert enter.exists(), "tools/enter.sh is missing"
    assert onboard.exists(), "tools/onboard.sh is missing"


def test_task_enter_wrapper_targets_qf() -> None:
    enter_text = (REPO_ROOT / "tools" / "enter.sh").read_text(encoding="utf-8")
    onboard_text = (REPO_ROOT / "tools" / "onboard.sh").read_text(encoding="utf-8")
    assert "python3 tools/init.py" in enter_text
    assert "tools/legacy.sh onboard" in onboard_text
