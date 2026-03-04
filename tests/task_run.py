from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_task_run_state_file_exists() -> None:
    state_file = REPO_ROOT / "TASKS" / "STATE.md"
    assert state_file.exists(), "TASKS/STATE.md is missing"
    text = state_file.read_text(encoding="utf-8")
    assert "CURRENT_RUN_ID:" in text


def test_task_run_scripts_reference_run_id() -> None:
    qf_text = (REPO_ROOT / "tools" / "qf").read_text(encoding="utf-8")
    ship_text = (REPO_ROOT / "tools" / "ship.sh").read_text(encoding="utf-8")
    assert "RUN_ID" in qf_text
    assert "run_id" in ship_text or "RUN_ID" in ship_text

