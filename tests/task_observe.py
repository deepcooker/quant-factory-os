from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_task_observe_script_exists() -> None:
    observe = REPO_ROOT / "tools" / "observe.sh"
    assert observe.exists(), "tools/observe.sh is missing"


def test_task_observe_requires_run_id() -> None:
    result = subprocess.run(
        ["bash", "tools/observe.sh"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "RUN_ID is required" in (result.stderr + result.stdout)

