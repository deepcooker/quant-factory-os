import os
import subprocess


def run_guard(file_list: str):
    env = os.environ.copy()
    env["SHIP_GUARD_ONLY"] = "1"
    env["SHIP_GUARD_FILE_LIST"] = file_list
    return subprocess.run(
        ["bash", "tools/ship.sh", "test: guard only"],
        env=env,
        text=True,
        capture_output=True,
    )


def test_guard_blocks_multiple_run_ids():
    files = "\n".join(
        [
            "reports/run-2026-02-21-a/meta.json",
            "reports/run-2026-02-21-b/meta.json",
            "TASKS/TASK-one.md",
        ]
    )
    res = run_guard(files)
    assert res.returncode != 0
    combined = (res.stdout or "") + (res.stderr or "")
    # Don't overfit exact wording; just require it mentions multiple RUN_ID or similar.
    assert ("RUN_ID" in combined) or ("多个" in combined)


def test_guard_blocks_multiple_task_files():
    files = "\n".join(
        [
            "reports/run-2026-02-21-a/meta.json",
            "TASKS/TASK-a.md",
            "TASKS/TASK-b.md",
        ]
    )
    res = run_guard(files)
    assert res.returncode != 0
    combined = (res.stdout or "") + (res.stderr or "")
    assert ("TASK" in combined) or ("任务" in combined) or ("多个" in combined)
