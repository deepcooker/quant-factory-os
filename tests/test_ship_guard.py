import os
import subprocess


def run_guard(
    file_list: str | None = None, allow_workflows: bool = False
) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["SHIP_GUARD_ONLY"] = "1"
    if file_list is not None:
        env["SHIP_GUARD_FILE_LIST"] = file_list
    if allow_workflows:
        env["SHIP_ALLOW_WORKFLOWS"] = "1"
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


def test_ship_guard_ignores_untracked_reports_when_staged_single_run():
    old_dir = os.path.join("reports", "run-guard-old")
    new_dir = os.path.join("reports", "run-guard-new")
    os.makedirs(old_dir, exist_ok=True)
    os.makedirs(new_dir, exist_ok=True)
    old_file = os.path.join(old_dir, "old.txt")
    new_file = os.path.join(new_dir, "new.txt")
    with open(old_file, "w", encoding="utf-8") as handle:
        handle.write("old\n")
    with open(new_file, "w", encoding="utf-8") as handle:
        handle.write("new\n")

    res = run_guard(f"{new_file}\n")
    os.remove(old_file)
    os.remove(new_file)
    try:
        os.rmdir(old_dir)
        os.rmdir(new_dir)
    except OSError:
        pass
    assert res.returncode == 0


def test_ship_guard_blocks_workflow_changes_by_default():
    res = run_guard(".github/workflows/ci.yml\n")
    assert res.returncode != 0
    combined = (res.stdout + res.stderr).strip()
    assert "workflow" in combined.lower()
    assert "SHIP_ALLOW_WORKFLOWS=1" in combined


def test_ship_guard_allows_workflow_changes_with_override():
    res = run_guard(".github/workflows/ci.yml\n", allow_workflows=True)
    assert res.returncode == 0
