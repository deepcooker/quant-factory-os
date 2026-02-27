import os
import shutil
import stat
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def setup_repo(tmp_path: Path) -> Path:
    repo_root = Path(__file__).resolve().parents[1]
    repo = tmp_path / "repo"
    (repo / "tools").mkdir(parents=True)
    (repo / "reports").mkdir(parents=True)
    (repo / "TASKS").mkdir(parents=True)
    shutil.copy2(repo_root / "tools" / "qf", repo / "tools" / "qf")
    mode = os.stat(repo / "tools" / "qf").st_mode
    os.chmod(repo / "tools" / "qf", mode | stat.S_IXUSR)

    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test User"], cwd=repo)
    return repo


def write_state(repo: Path, run_id: str, task_file: str = "TASKS/TASK-a.md", status: str = "active") -> None:
    (repo / "TASKS" / "STATE.md").write_text(
        "\n".join(
            [
                "# STATE",
                f"CURRENT_RUN_ID: {run_id}",
                f"CURRENT_TASK_FILE: {task_file}",
                f"CURRENT_STATUS: {status}",
                "",
                "## Current baseline",
                "- test",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_qf_ready_defaults_to_current_run_id(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    write_state(repo, "run-current")
    env = os.environ.copy()
    env["QF_READY_GOAL"] = "goal"
    env["QF_READY_SCOPE"] = "scope"
    env["QF_READY_ACCEPTANCE"] = "accept"
    env["QF_READY_STEPS"] = "steps"
    env["QF_READY_STOP"] = "stop"
    res = run(["bash", "tools/qf", "ready"], cwd=repo, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert (repo / "reports" / "run-current" / "ready.json").exists()
    assert "READY_RUN_ID: run-current" in res.stdout


def test_qf_ready_fails_on_run_id_mismatch(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    write_state(repo, "run-current")
    env = os.environ.copy()
    env["QF_READY_GOAL"] = "goal"
    env["QF_READY_SCOPE"] = "scope"
    env["QF_READY_ACCEPTANCE"] = "accept"
    env["QF_READY_STEPS"] = "steps"
    env["QF_READY_STOP"] = "stop"
    res = run(["bash", "tools/qf", "ready", "RUN_ID=run-other"], cwd=repo, env=env)
    assert res.returncode != 0
    combined = res.stdout + res.stderr
    assert "run-id mismatch" in combined
    assert "CURRENT_RUN_ID" in combined


def test_qf_handoff_defaults_to_current_run_id(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    write_state(repo, "run-current")
    out_dir = repo / "reports" / "run-current"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "ready.json").write_text('{"restatement_passed": true, "restatement": {}}', encoding="utf-8")
    res = run(["bash", "tools/qf", "handoff"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "HANDOFF_RUN_ID: run-current" in res.stdout
    assert (out_dir / "handoff.md").exists()


def test_qf_do_updates_current_run_pointer_after_pick(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    write_state(repo, "run-current", "TASKS/TASK-old.md", "active")
    (repo / "reports" / "run-current").mkdir(parents=True, exist_ok=True)
    (repo / "reports" / "run-current" / "ready.json").write_text('{"restatement_passed": true}', encoding="utf-8")
    (repo / "TASKS" / "TODO_PROPOSAL.md").write_text("# proposal\n", encoding="utf-8")

    task_script = repo / "tools" / "task.sh"
    task_script.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "echo 'TASK_FILE: TASKS/TASK-picked.md'",
                "echo 'RUN_ID: run-picked'",
                "echo 'EVIDENCE_PATH: reports/run-picked/'",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    os.chmod(task_script, os.stat(task_script).st_mode | stat.S_IXUSR)
    run(["git", "add", "."], cwd=repo)
    run(["git", "commit", "-m", "seed"], cwd=repo)

    env = os.environ.copy()
    env["QF_SKIP_SYNC"] = "1"
    res = run(["bash", "tools/qf", "do", "queue-next"], cwd=repo, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    state = (repo / "TASKS" / "STATE.md").read_text(encoding="utf-8")
    assert "CURRENT_RUN_ID: run-picked" in state
    assert "CURRENT_TASK_FILE: TASKS/TASK-picked.md" in state


def test_qf_resume_defaults_to_current_run_id(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    write_state(repo, "run-current")
    res = run(["bash", "tools/qf", "resume"], cwd=repo)
    assert res.returncode != 0
    combined = res.stdout + res.stderr
    assert "missing state file" in combined
    assert "reports/run-current/ship_state.json" in combined
