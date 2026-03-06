from __future__ import annotations

import os
import subprocess
import json
from pathlib import Path

from tools.learn import parse_cli


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


def test_ready_writes_legacy_compatible_fields(tmp_path: Path) -> None:
    tasks_dir = tmp_path / "TASKS"
    reports_dir = tmp_path / "reports"
    tasks_dir.mkdir()
    reports_dir.mkdir()

    state_file = tasks_dir / "STATE.md"
    task_file = tasks_dir / "TASK-test.md"
    run_id = "run-test-ready-compat"
    project_id = "project-0"

    state_file.write_text(
        "\n".join(
            [
                f"CURRENT_PROJECT_ID: {project_id}",
                f"CURRENT_RUN_ID: {run_id}",
                f"CURRENT_TASK_FILE: {task_file.relative_to(tmp_path)}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    task_file.write_text(
        "\n".join(
            [
                "# TASK: ready compatibility",
                "",
                "## Goal",
                "验证 ready 最小 schema 仍兼容 legacy gate。",
                "",
                "## Scope",
                "- `tools/ready.py`",
                "",
                "## Acceptance",
                "- [ ] `ready.json` 同时包含新版 contract 和旧版兼容字段",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["QF_STATE_FILE"] = str(state_file)
    env["QF_READY_REQUIRE_LEARN"] = "0"
    env["QF_READY_REQUIRE_SYNC"] = "0"

    result = subprocess.run(
        ["python3", str(READY_PATH), f"RUN_ID={run_id}"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )

    assert result.returncode == 0, result.stderr
    ready_path = tmp_path / "reports" / run_id / "ready.json"
    ready_obj = json.loads(ready_path.read_text(encoding="utf-8"))

    assert ready_obj["schema"] == "qf_ready.v2"
    assert ready_obj["restatement_passed"] is True
    assert ready_obj["learn_gate"]["learn_passed"] is True
    assert ready_obj["sync_gate"]["sync_passed"] is True
    assert ready_obj["restatement"]["goal"] == ready_obj["contract"]["goal"]
    assert ready_obj["restatement"]["scope"] == ready_obj["contract"]["scope"]
    assert ready_obj["restatement"]["acceptance"] == ready_obj["contract"]["acceptance"]


def test_learn_daily_alias_maps_to_medium() -> None:
    cfg = parse_cli(["-daily"])

    assert cfg["reasoning_alias"] == "daily"
    assert cfg["reasoning_profile"] == "medium"
    assert cfg["model_reasoning_effort"] == "medium"
