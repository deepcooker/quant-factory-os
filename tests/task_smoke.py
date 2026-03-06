from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SMOKE_PATH = REPO_ROOT / "tools" / "smoke.sh"


def test_task_smoke_script_exists() -> None:
    assert SMOKE_PATH.exists(), "tools/smoke.sh is missing"


def test_task_smoke_passes_on_ready_run(tmp_path: Path) -> None:
    tasks_dir = tmp_path / "TASKS"
    reports_dir = tmp_path / "reports"
    run_id = "run-test-smoke-pass"
    task_rel = "TASKS/TASK-test.md"

    tasks_dir.mkdir()
    (reports_dir / run_id).mkdir(parents=True)

    (tasks_dir / "STATE.md").write_text(
        "\n".join(
            [
                "CURRENT_PROJECT_ID: project-0",
                f"CURRENT_RUN_ID: {run_id}",
                f"CURRENT_TASK_FILE: {task_rel}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (tasks_dir / "TASK-test.md").write_text("# TASK: smoke pass\n", encoding="utf-8")
    (reports_dir / run_id / "summary.md").write_text("make verify\n", encoding="utf-8")
    (reports_dir / run_id / "decision.md").write_text("task_done\n", encoding="utf-8")
    (reports_dir / run_id / "meta.json").write_text("{}", encoding="utf-8")
    review_obj = {
        "status": "pass",
        "blockers_count": 0,
    }
    (reports_dir / run_id / "drift_review.json").write_text(
        json.dumps(review_obj), encoding="utf-8"
    )
    (reports_dir / run_id / "drift_review.md").write_text("# Drift Review\n", encoding="utf-8")

    result = subprocess.run(
        ["bash", str(SMOKE_PATH)],
        cwd=tmp_path,
        env={**os.environ, "QF_STATE_FILE": str(tasks_dir / "STATE.md")},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "SMOKE_STATUS: pass" in result.stdout
    smoke_obj = json.loads((reports_dir / run_id / "smoke.json").read_text(encoding="utf-8"))
    assert smoke_obj["status"] == "pass"
    assert smoke_obj["missing_items"] == []


def test_task_smoke_fails_when_review_missing(tmp_path: Path) -> None:
    tasks_dir = tmp_path / "TASKS"
    reports_dir = tmp_path / "reports"
    run_id = "run-test-smoke-fail"
    task_rel = "TASKS/TASK-test.md"

    tasks_dir.mkdir()
    (reports_dir / run_id).mkdir(parents=True)

    (tasks_dir / "STATE.md").write_text(
        "\n".join(
            [
                "CURRENT_PROJECT_ID: project-0",
                f"CURRENT_RUN_ID: {run_id}",
                f"CURRENT_TASK_FILE: {task_rel}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (tasks_dir / "TASK-test.md").write_text("# TASK: smoke fail\n", encoding="utf-8")
    (reports_dir / run_id / "summary.md").write_text("make verify\n", encoding="utf-8")
    (reports_dir / run_id / "decision.md").write_text("needs_human_decision\n", encoding="utf-8")
    (reports_dir / run_id / "meta.json").write_text("{}", encoding="utf-8")

    result = subprocess.run(
        ["bash", str(SMOKE_PATH)],
        cwd=tmp_path,
        env={**os.environ, "QF_STATE_FILE": str(tasks_dir / "STATE.md")},
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0
    assert "SMOKE_STATUS: fail" in result.stdout
    assert "SMOKE_MISSING_ITEM_1" in result.stdout
