from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_task_ship_script_exists() -> None:
    ship = REPO_ROOT / "tools" / "ship.sh"
    assert ship.exists(), "tools/ship.sh is missing"


def test_task_ship_usage_without_message() -> None:
    result = subprocess.run(
        ["bash", "tools/ship.sh"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "用法：tools/ship.sh" in (result.stderr + result.stdout)

