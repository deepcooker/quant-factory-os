import os
import subprocess
from pathlib import Path

def test_bootstrap_scope_extracts_backticked_paths(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    queue_file = tmp_path / "QUEUE.md"
    template_file = tmp_path / "_TEMPLATE.md"
    output_dir = tmp_path / "TASKS_OUT"

    queue_file.write_text(
        "\n".join([
            "# QUEUE", "", "## Queue",
            "- [ ] TODO Title: scope extract",
            "  Goal: test",
            "  Scope: `tools/task.sh`, `tests/`, `TASKS/QUEUE.md`",
        ]),
        encoding="utf-8",
    )
    template_file.write_text("# TASK: x\n\nRUN_ID: x\nOWNER: x\nPRIORITY: P1\n", encoding="utf-8")

    env = os.environ.copy()
    env["TASK_BOOTSTRAP_QUEUE_FILE"] = str(queue_file)
    env["TASK_BOOTSTRAP_TEMPLATE_FILE"] = str(template_file)
    env["TASK_BOOTSTRAP_OUTPUT_DIR"] = str(output_dir)
    env["TASK_BOOTSTRAP_EVIDENCE_CMD"] = "true"

    res = subprocess.run(["bash", "tools/task.sh", "--next"], cwd=repo_root, env=env, text=True, capture_output=True)
    assert res.returncode == 0, res.stdout + res.stderr

    # verify generated task has bullets for each path and does not contain `, `
    task_path = None
    for line in (res.stdout + res.stderr).splitlines():
        if line.strip().startswith("TASK_FILE:"):
            task_path = line.split(":", 1)[1].strip()
    assert task_path, res.stdout + res.stderr

    content = (repo_root / task_path).read_text(encoding="utf-8")
    assert "- `tools/task.sh`" in content
    assert "- `tests/`" in content
    assert "- `TASKS/QUEUE.md`" in content
    assert "` , `" not in content
    assert "` ,`" not in content
    assert "`," not in content
