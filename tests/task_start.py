from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_task_start_script_exists() -> None:
    start = REPO_ROOT / "tools" / "start.sh"
    doctor = REPO_ROOT / "tools" / "doctor.sh"
    assert start.exists(), "tools/start.sh is missing"
    assert doctor.exists(), "tools/doctor.sh is missing"


def test_task_start_contains_dry_run_and_codex_entry() -> None:
    text = (REPO_ROOT / "tools" / "start.sh").read_text(encoding="utf-8")
    assert "START_DRY_RUN" in text
    assert "exec codex" in text

