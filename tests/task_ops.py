from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INIT_PATH = REPO_ROOT / "tools" / "init.py"
LEARN_PATH = REPO_ROOT / "tools" / "learn.py"
READY_PATH = REPO_ROOT / "tools" / "ready.py"


def _run_init_status() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "-lc", "python3 tools/init.py -status"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_task_scripts_exist() -> None:
    assert INIT_PATH.exists(), "tools/init.py is missing"
    assert LEARN_PATH.exists(), "tools/learn.py is missing"
    assert READY_PATH.exists(), "tools/ready.py is missing"
    assert os.access(INIT_PATH, os.X_OK), "tools/init.py is not executable"


def test_task_init_status_smoke() -> None:
    result = _run_init_status()
    assert result.returncode == 0
    assert "INIT_STEP[1/7]" in result.stdout
    assert "INIT_STATUS:" in result.stdout
