import os
import re
import subprocess
from pathlib import Path


def run_next(tmp_dir: Path, queue_text: str):
    tmp_dir.mkdir(parents=True, exist_ok=True)

    queue = tmp_dir / "QUEUE.md"
    queue.write_text(queue_text, encoding="utf-8")

    template = tmp_dir / "_TEMPLATE.md"
    template.write_text("# TEMPLATE\n", encoding="utf-8")

    env = os.environ.copy()
    env["TASK_BOOTSTRAP_QUEUE_FILE"] = str(queue)
    env["TASK_BOOTSTRAP_TEMPLATE_FILE"] = str(template)
    env["TASK_BOOTSTRAP_OUTPUT_DIR"] = str(tmp_dir)

    res = subprocess.run(
        ["bash", "tools/task.sh", "--next"],
        env=env,
        text=True,
        capture_output=True,
    )
    return res, queue


def test_next_marks_queue_item_in_progress_and_records_picked():
    q = (
        "# QUEUE\n\n## Queue\n"
        "- [ ] TODO Title: queue pick lock (in-progress marker)\n"
        "  Goal: test\n"
        "  Scope: `tools/task.sh`, `TASKS/QUEUE.md`, `tests/`\n"
    )
    #res, queue = run_next(Path(os.getenv("TMPDIR", "/tmp")) and Path(os.getenv("TMPDIR", "/tmp")) / "qpl1", q)
    # Use a unique temp dir per test run
    tmp_dir = Path(os.getenv("TMPDIR", "/tmp")) / "qpl1"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    res, queue = run_next(tmp_dir, q)

    
    
    #tmp_dir = queue.parent
    tmp_dir.mkdir(parents=True, exist_ok=True)
    res, queue = run_next(tmp_dir, q)

    assert res.returncode == 0, (res.stdout + res.stderr)

    updated = queue.read_text(encoding="utf-8")
    assert "- [>]" in updated
    assert "Picked:" in updated

    # Should include the generated RUN_ID somewhere on the picked line
    m = re.search(r"RUN_ID:\s*(run-[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+)", res.stdout + res.stderr)
    assert m, (res.stdout + res.stderr)
    assert m.group(1) in updated


def test_next_does_not_pick_in_progress_item_again():
    q = (
        "# QUEUE\n\n## Queue\n"
        "- [ ] TODO Title: queue pick lock (in-progress marker)\n"
        "  Goal: test\n"
        "  Scope: `tools/task.sh`, `TASKS/QUEUE.md`, `tests/`\n"
    )
    tmp_dir = Path(os.getenv("TMPDIR", "/tmp")) / "qpl2"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    res1, queue = run_next(tmp_dir, q)
    assert res1.returncode == 0, (res1.stdout + res1.stderr)

    # Second run should NOT pick the same item again; should report no unfinished item
    res2, _ = run_next(tmp_dir, queue.read_text(encoding="utf-8"))
    assert res2.returncode != 0
    combined = (res2.stdout or "") + (res2.stderr or "")
    assert "没有未完成项" in combined or "QUEUE" in combined
