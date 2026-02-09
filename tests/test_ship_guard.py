import os
import subprocess


def run_guard(file_list: str) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["SHIP_GUARD_ONLY"] = "1"
    env["SHIP_GUARD_FILE_LIST"] = file_list
    return subprocess.run(
        ["bash", "tools/ship.sh", "test: ship guard"],
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def test_ship_guard_blocks_multiple_runs():
    res = run_guard("reports/run-a/meta.json\nreports/run-b/summary.md\n")
    assert res.returncode != 0
    combined = (res.stdout + res.stderr).strip()
    assert "单任务单 RUN_ID" in combined


def test_ship_guard_blocks_multiple_tasks():
    res = run_guard("TASKS/TASK-a.md\nTASKS/TASK-b.md\n")
    assert res.returncode != 0
    combined = (res.stdout + res.stderr).strip()
    assert "单任务单 RUN_ID" in combined


def test_ship_guard_allows_single_run_and_task():
    res = run_guard("reports/run-a/meta.json\nTASKS/TASK-a.md\n")
    assert res.returncode == 0
