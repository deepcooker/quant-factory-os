import os
import subprocess
from pathlib import Path


def test_start_script_missing_venv(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "tools" / "start.sh"
    missing_venv = tmp_path / "missing-venv"

    env = os.environ.copy()
    env["START_VENV_PATH"] = str(missing_venv)
    env["START_DRY_RUN"] = "1"

    result = subprocess.run(
        ["bash", str(script)],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    assert result.returncode != 0
    combined = (result.stdout + result.stderr).lower()
    assert "venv" in combined
    assert "start_venv_path" in combined
