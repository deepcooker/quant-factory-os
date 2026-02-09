import os
import subprocess
from pathlib import Path


def run_probe(tmp_path, script, run_id):
    env = os.environ.copy()
    env["RUN_ID"] = run_id
    return subprocess.run(
        [
            "python3",
            str(script),
            "--run-id",
            run_id,
            "--a9-root",
            str(tmp_path),
            "--mode",
            "probe",
        ],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_probe_fails_without_main_controller(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "tools" / "run_a9.py"
    run_id = "run-probe-missing-controller"

    result = run_probe(tmp_path, script, run_id)

    assert result.returncode != 0
    combined = (result.stdout + result.stderr).lower()
    assert "main_controller.py" in combined


def test_probe_succeeds_with_main_controller(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "tools" / "run_a9.py"
    run_id = "run-probe-ok"

    main_controller = tmp_path / "main_controller.py"
    main_controller.write_text(
        "import argparse\n"
        "argparse.ArgumentParser().parse_args()\n",
        encoding="utf-8",
    )

    result = run_probe(tmp_path, script, run_id)

    assert result.returncode == 0
    log_path = repo_root / "reports" / run_id / "a9_stdout.log"
    assert log_path.exists()
