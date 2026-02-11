import os
import subprocess
from pathlib import Path


def run_scope_gate_only(task_file: Path, files: str, run_id: str = "run-test-scope-gate"):
    env = os.environ.copy()
    env["SHIP_SCOPE_GATE_ONLY"] = "1"
    env["SHIP_SCOPE_GATE_TASK_FILE"] = str(task_file)
    env["SHIP_SCOPE_GATE_FILES"] = files
    env["SHIP_SCOPE_GATE_RUN_ID"] = run_id
    return subprocess.run(
        ["bash", "tools/ship.sh", "test: ship scope gate"],
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def test_scope_gate_allows_files_within_declared_scope(tmp_path):
    task_file = tmp_path / "TASK-scope-ok.md"
    task_file.write_text(
        "\n".join(
            [
                "# TASK: scope gate fixture",
                "RUN_ID: run-test-scope-gate",
                "",
                "## Scope",
                "- `tools/ship.sh`",
                "- `tests/`",
                "",
                "## Goal",
                "-",
            ]
        ),
        encoding="utf-8",
    )

    files = "\n".join(
        [
            "tools/ship.sh",
            "tests/test_ship_scope_gate.py",
            "reports/run-test-scope-gate/summary.md",
            str(task_file),
        ]
    )
    res = run_scope_gate_only(task_file, files)
    assert res.returncode == 0, (res.stdout + res.stderr)


def test_scope_gate_blocks_out_of_scope_files(tmp_path):
    task_file = tmp_path / "TASK-scope-block.md"
    task_file.write_text(
        "\n".join(
            [
                "# TASK: scope gate fixture",
                "RUN_ID: run-test-scope-gate",
                "",
                "## Scope",
                "- `tools/ship.sh`",
                "- `tests/`",
                "",
                "## Goal",
                "-",
            ]
        ),
        encoding="utf-8",
    )

    files = "\n".join(
        [
            "tools/ship.sh",
            "write.py",
            str(task_file),
        ]
    )
    res = run_scope_gate_only(task_file, files)
    combined = (res.stdout + res.stderr).lower()
    assert res.returncode != 0
    assert "out-of-scope" in combined
    assert "write.py" in combined
