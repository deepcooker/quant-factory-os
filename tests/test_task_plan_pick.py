import os
import re
import subprocess
from pathlib import Path


def test_task_plan_generates_proposal_with_queue_next_and_recent_decisions(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    queue_file = tmp_path / "QUEUE.md"
    reports_dir = tmp_path / "reports"
    proposal_file = tmp_path / "TODO_PROPOSAL.md"

    queue_file.write_text(
        "\n".join(
            [
                "# QUEUE",
                "",
                "## Queue",
                "- [ ] TODO Title: first candidate",
                "- [ ] TODO Title: second candidate",
            ]
        ),
        encoding="utf-8",
    )
    (reports_dir / "run-a").mkdir(parents=True)
    (reports_dir / "run-b").mkdir(parents=True)
    (reports_dir / "run-a" / "decision.md").write_text("# Decision A\n", encoding="utf-8")
    (reports_dir / "run-b" / "decision.md").write_text("# Decision B\n", encoding="utf-8")

    env = os.environ.copy()
    env["TASK_PLAN_QUEUE_FILE"] = str(queue_file)
    env["TASK_PLAN_REPORTS_DIR"] = str(reports_dir)
    env["TASK_PLAN_OUTPUT_FILE"] = str(proposal_file)

    res = subprocess.run(
        ["bash", "tools/task.sh", "--plan", "10"],
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert res.returncode == 0, res.stdout + res.stderr
    assert proposal_file.exists()
    assert "PROPOSAL_FILE:" in res.stdout
    assert "--pick queue-next" in res.stdout

    content = proposal_file.read_text(encoding="utf-8")
    assert "## Queue candidates" in content
    assert "id=queue-next" in content
    assert "## Recent decisions" in content
    assert "decision.md" in content


def test_task_pick_queue_next_outputs_task_file_and_run_id(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    queue_file = tmp_path / "QUEUE.md"
    template_file = tmp_path / "_TEMPLATE.md"
    output_dir = tmp_path / "TASKS_OUT"
    proposal_file = tmp_path / "TODO_PROPOSAL.md"

    queue_file.write_text(
        "\n".join(
            [
                "# QUEUE",
                "",
                "## Queue",
                "- [ ] TODO Title: pick candidate",
                "  Goal: test",
                "  Scope: tests/",
            ]
        ),
        encoding="utf-8",
    )
    template_file.write_text("# TASK: x\n\nRUN_ID: x\nOWNER: x\nPRIORITY: P1\n", encoding="utf-8")
    proposal_file.write_text("# TODO Proposal\n", encoding="utf-8")

    env = os.environ.copy()
    env["TASK_BOOTSTRAP_QUEUE_FILE"] = str(queue_file)
    env["TASK_BOOTSTRAP_TEMPLATE_FILE"] = str(template_file)
    env["TASK_BOOTSTRAP_OUTPUT_DIR"] = str(output_dir)
    env["TASK_PLAN_OUTPUT_FILE"] = str(proposal_file)
    env["TASK_BOOTSTRAP_EVIDENCE"] = "0"

    res = subprocess.run(
        ["bash", "tools/task.sh", "--pick", "queue-next"],
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert res.returncode == 0, res.stdout + res.stderr
    assert re.search(r"^TASK_FILE:\s+.+$", res.stdout, flags=re.MULTILINE)
    assert re.search(r"^RUN_ID:\s+run-[0-9]{4}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+$", res.stdout, flags=re.MULTILINE)


def test_task_plan_includes_suggested_tasks_when_queue_empty(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    queue_file = tmp_path / "QUEUE.md"
    reports_dir = tmp_path / "reports"
    state_file = tmp_path / "STATE.md"
    mistakes_dir = tmp_path / "MISTAKES"
    proposal_file = tmp_path / "TODO_PROPOSAL.md"

    queue_file.write_text(
        "\n".join(
            [
                "# QUEUE",
                "",
                "## Queue",
            ]
        ),
        encoding="utf-8",
    )
    (reports_dir / "run-z").mkdir(parents=True)
    (reports_dir / "run-z" / "decision.md").write_text(
        "\n".join(
            [
                "## Risks",
                "- rollback may be needed",
            ]
        ),
        encoding="utf-8",
    )
    state_file.write_text("Current risk: queue is empty\n", encoding="utf-8")
    mistakes_dir.mkdir(parents=True)
    (mistakes_dir / "m1.md").write_text("recurring issue\n", encoding="utf-8")

    env = os.environ.copy()
    env["TASK_PLAN_QUEUE_FILE"] = str(queue_file)
    env["TASK_PLAN_REPORTS_DIR"] = str(reports_dir)
    env["TASK_PLAN_STATE_FILE"] = str(state_file)
    env["TASK_PLAN_MISTAKES_DIR"] = str(mistakes_dir)
    env["TASK_PLAN_OUTPUT_FILE"] = str(proposal_file)

    res = subprocess.run(
        ["bash", "tools/task.sh", "--plan", "20"],
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert res.returncode == 0, res.stdout + res.stderr
    content = proposal_file.read_text(encoding="utf-8")
    assert "## Queue candidates" in content
    assert "- (none)" in content
    assert "## Suggested tasks" in content
    assert content.count("TODO Title:") >= 5
    assert "Goal:" in content
    assert "Scope:" in content
    assert "Acceptance:" in content
