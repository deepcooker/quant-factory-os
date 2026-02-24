import os
import subprocess
from pathlib import Path


def _prepare_minimal_queue(tmp_path: Path):
    queue_file = tmp_path / "QUEUE.md"
    template_file = tmp_path / "_TEMPLATE.md"
    output_dir = tmp_path / "TASKS_OUT"

    queue_file.write_text(
        "\n".join(
            [
                "# QUEUE",
                "",
                "## Queue",
                "- [ ] TODO Title: auto evidence pick",
                "  Goal: test",
                "  Scope: tests/",
            ]
        ),
        encoding="utf-8",
    )
    template_file.write_text("# TASK: x\n\nRUN_ID: x\nOWNER: x\nPRIORITY: P1\n", encoding="utf-8")
    return queue_file, template_file, output_dir


def test_next_auto_evidence_success_prints_checklist_and_evidence(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    queue_file, template_file, output_dir = _prepare_minimal_queue(tmp_path)

    env = os.environ.copy()
    env["TASK_BOOTSTRAP_QUEUE_FILE"] = str(queue_file)
    env["TASK_BOOTSTRAP_TEMPLATE_FILE"] = str(template_file)
    env["TASK_BOOTSTRAP_OUTPUT_DIR"] = str(output_dir)
    env["TASK_BOOTSTRAP_EVIDENCE_CMD"] = "true"

    res = subprocess.run(
        ["bash", "tools/task.sh", "--next"],
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert res.returncode == 0, res.stdout + res.stderr

    combined = (res.stdout or "") + (res.stderr or "")
    assert "TASK_FILE:" in combined
    assert "RUN_ID:" in combined
    assert "EVIDENCE_PATH:" in combined
    assert "== 下一步清单 ==" in combined
    assert "tools/view.sh" in combined
    assert "make verify" in combined

    updated = queue_file.read_text(encoding="utf-8")
    assert "- [>]" in updated


def test_next_auto_evidence_failure_rolls_back_queue_marker(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    queue_file, template_file, output_dir = _prepare_minimal_queue(tmp_path)
    before = queue_file.read_text(encoding="utf-8")

    env = os.environ.copy()
    env["TASK_BOOTSTRAP_QUEUE_FILE"] = str(queue_file)
    env["TASK_BOOTSTRAP_TEMPLATE_FILE"] = str(template_file)
    env["TASK_BOOTSTRAP_OUTPUT_DIR"] = str(output_dir)
    env["TASK_BOOTSTRAP_EVIDENCE_CMD"] = "false"

    res = subprocess.run(
        ["bash", "tools/task.sh", "--next"],
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert res.returncode != 0
    combined = (res.stdout or "") + (res.stderr or "")
    assert "Auto evidence failed" in combined

    after = queue_file.read_text(encoding="utf-8")
    assert after == before
    assert "- [>]" not in after
