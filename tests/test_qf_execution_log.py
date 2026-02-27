import json
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


def test_qf_do_writes_execution_log(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    task_script = repo / "tools" / "task.sh"
    task_script.write_text(
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        "if [[ \"${1:-}\" == \"--pick\" ]]; then\n"
        "  echo \"TASK_FILE: TASKS/TASK-picked.md\"\n"
        "  echo \"RUN_ID: run-picked\"\n"
        "  echo \"EVIDENCE_PATH: reports/run-picked\"\n"
        "  exit 0\n"
        "fi\n"
        "exit 1\n",
        encoding="utf-8",
    )
    os.chmod(task_script, os.stat(task_script).st_mode | stat.S_IXUSR)
    (repo / "TASKS" / "TODO_PROPOSAL.md").write_text("# proposal\n", encoding="utf-8")

    run(["git", "add", "."], cwd=repo)
    run(["git", "commit", "-m", "seed"], cwd=repo)

    env = os.environ.copy()
    env["QF_READY_GOAL"] = "one goal"
    env["QF_READY_SCOPE"] = "tools/qf"
    env["QF_READY_ACCEPTANCE"] = "make verify"
    env["QF_READY_STEPS"] = "init ready do"
    env["QF_READY_STOP"] = "wait"
    ready = run(["bash", "tools/qf", "ready", "RUN_ID=run-ready"], cwd=repo, env=env)
    assert ready.returncode == 0, ready.stdout + ready.stderr

    env["QF_SKIP_SYNC"] = "1"
    do = run(["bash", "tools/qf", "do", "queue-next"], cwd=repo, env=env)
    assert do.returncode == 0, do.stdout + do.stderr

    ready_log = repo / "reports" / "run-ready" / "execution.jsonl"
    picked_log = repo / "reports" / "run-picked" / "execution.jsonl"
    assert ready_log.exists()
    assert picked_log.exists()
    assert "do_start" in ready_log.read_text(encoding="utf-8")
    assert "do_pick_success" in picked_log.read_text(encoding="utf-8")


def test_qf_resume_missing_state_writes_failure_event(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    res = run(["bash", "tools/qf", "resume", "RUN_ID=run-missing"], cwd=repo)
    assert res.returncode != 0
    log_file = repo / "reports" / "run-missing" / "execution.jsonl"
    assert log_file.exists()
    items = [json.loads(x) for x in log_file.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert any(x.get("action") == "resume_missing_state" and x.get("status") == "fail" for x in items)


def test_qf_execution_log_redacts_token_text(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    task_script = repo / "tools" / "task.sh"
    task_script.write_text(
        "#!/usr/bin/env bash\n"
        "set -euo pipefail\n"
        "echo \"token=abc123 password=xyz Authorization: Bearer secrettoken\" >&2\n"
        "exit 1\n",
        encoding="utf-8",
    )
    os.chmod(task_script, os.stat(task_script).st_mode | stat.S_IXUSR)
    (repo / "TASKS" / "TODO_PROPOSAL.md").write_text("# proposal\n", encoding="utf-8")
    run(["git", "add", "."], cwd=repo)
    run(["git", "commit", "-m", "seed"], cwd=repo)

    env = os.environ.copy()
    env["QF_READY_GOAL"] = "goal"
    env["QF_READY_SCOPE"] = "scope"
    env["QF_READY_ACCEPTANCE"] = "accept"
    env["QF_READY_STEPS"] = "steps"
    env["QF_READY_STOP"] = "stop"
    ready = run(["bash", "tools/qf", "ready", "RUN_ID=run-redact"], cwd=repo, env=env)
    assert ready.returncode == 0

    env["QF_SKIP_SYNC"] = "1"
    do = run(["bash", "tools/qf", "do", "queue-next"], cwd=repo, env=env)
    assert do.returncode != 0

    content = (repo / "reports" / "run-redact" / "execution.jsonl").read_text(encoding="utf-8")
    assert "token=<redacted>" in content
    assert "password=<redacted>" in content
    assert "Bearer <redacted>" in content
