from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_task_view_script_exists() -> None:
    view = REPO_ROOT / "tools" / "view.sh"
    assert view.exists(), "tools/view.sh is missing"


def test_task_view_usage_without_args() -> None:
    result = subprocess.run(
        ["bash", "tools/view.sh"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "Usage: tools/view.sh" in (result.stderr + result.stdout)

