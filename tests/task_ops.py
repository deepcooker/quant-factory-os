from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
OPS_PATH = REPO_ROOT / "tools" / "ops"


def _run_ops_help() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "-lc", "tools/ops -h"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_task_ops_script_exists_and_executable() -> None:
    assert OPS_PATH.exists(), "tools/ops is missing"
    assert os.access(OPS_PATH, os.X_OK), "tools/ops is not executable"


def test_task_ops_help_smoke() -> None:
    result = _run_ops_help()
    assert "Usage:" in result.stdout
    assert "tools/ops init" in result.stdout
    assert "tools/ops learn" in result.stdout
    assert "tools/ops ready" in result.stdout
