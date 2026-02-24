import os
import re
import subprocess
from pathlib import Path


def test_task_bootstrap_next_generates_task_file(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    queue_file = tmp_path / "QUEUE.md"
    template_file = tmp_path / "_TEMPLATE.md"
    output_dir = tmp_path / "TASKS_OUT"

    queue_file.write_text(
        "\n".join(
            [
                "# QUEUE",
                "",
                "## Queue",
                "- [ ] TODO Title: smoke bootstrap task generator",
                "  Goal: generate a runnable task file from queue.",
                "  Scope: tests/",
                "  Acceptance:",
                "  - [ ] Command(s) pass: `make verify`",
                "  - [ ] Evidence updated: `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`",
                "  - [ ] No changes outside declared scope.",
                "",
                "- [x] TODO Title: done item",
            ]
        ),
        encoding="utf-8",
    )

    template_file.write_text(
        "\n".join(
            [
                "# TASK: <short-name>",
                "",
                "RUN_ID: <YYYY-MM-DD-identifier>",
                "OWNER: <you>",
                "PRIORITY: P1",
            ]
        ),
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["TASK_BOOTSTRAP_QUEUE_FILE"] = str(queue_file)
    env["TASK_BOOTSTRAP_TEMPLATE_FILE"] = str(template_file)
    env["TASK_BOOTSTRAP_OUTPUT_DIR"] = str(output_dir)
    env["TASK_BOOTSTRAP_EVIDENCE_CMD"] = "true"

    res = subprocess.run(
        ["bash", "tools/task.sh", "--next"],
        cwd=repo_root,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, (res.stdout + res.stderr)

    task_match = re.search(r"^TASK_FILE:\s+(.+)$", res.stdout, flags=re.MULTILINE)
    run_match = re.search(r"^RUN_ID:\s+(run-[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+)$", res.stdout, flags=re.MULTILINE)
    assert task_match is not None, res.stdout
    assert run_match is not None, res.stdout

    task_file = Path(task_match.group(1).strip())
    run_id = run_match.group(1).strip()
    assert task_file.exists()
    assert "YYYY" not in run_id

    content = task_file.read_text(encoding="utf-8")
    assert f"RUN_ID: {run_id}" in content
    assert "## Scope (Required)" in content
    assert "- `tests/`" in content
