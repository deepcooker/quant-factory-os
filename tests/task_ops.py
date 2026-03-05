from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OPS_INIT_PATH = REPO_ROOT / "tools" / "ops_init.py"
OPS_LEARN_PATH = REPO_ROOT / "tools" / "ops_learn.py"
OPS_READY_PATH = REPO_ROOT / "tools" / "ops_ready.py"


def _run_ops_init_status() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "-lc", "python3 tools/ops_init.py -status"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_task_ops_scripts_exist() -> None:
    assert OPS_INIT_PATH.exists(), "tools/ops_init.py is missing"
    assert OPS_LEARN_PATH.exists(), "tools/ops_learn.py is missing"
    assert OPS_READY_PATH.exists(), "tools/ops_ready.py is missing"
    assert os.access(OPS_INIT_PATH, os.X_OK), "tools/ops_init.py is not executable"


def test_task_ops_init_status_smoke() -> None:
    result = _run_ops_init_status()
    assert result.returncode == 0
    assert "INIT_STEP[1/7]" in result.stdout
    assert "INIT_STATUS:" in result.stdout
