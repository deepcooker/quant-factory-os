from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
QF_PATH = REPO_ROOT / "tools" / "qf"


def _run_qf_help() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "-lc", "tools/qf -h"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_task_qf_script_exists_and_executable() -> None:
    assert QF_PATH.exists(), "tools/qf is missing"
    assert os.access(QF_PATH, os.X_OK), "tools/qf is not executable"


def test_task_qf_help_smoke() -> None:
    result = _run_qf_help()
    assert result.returncode == 0, result.stderr
    assert "Usage:" in result.stdout
    assert "tools/qf init" in result.stdout
    assert "tools/qf learn" in result.stdout
    assert "tools/qf ready" in result.stdout

