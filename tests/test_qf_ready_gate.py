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

    shutil.copy2(repo_root / "tools" / "qf", repo / "tools" / "qf")
    mode = os.stat(repo / "tools" / "qf").st_mode
    os.chmod(repo / "tools" / "qf", mode | stat.S_IXUSR)

    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test User"], cwd=repo)
    return repo


def test_qf_do_requires_ready_gate(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    env = os.environ.copy()
    env["QF_SKIP_SYNC"] = "1"
    res = run(["bash", "tools/qf", "do", "queue-next"], cwd=repo, env=env)
    assert res.returncode != 0
    combined = res.stdout + res.stderr
    assert "readiness gate not satisfied" in combined
    assert "tools/qf ready" in combined


def test_qf_ready_writes_marker_from_env(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    env = os.environ.copy()
    env["QF_READY_GOAL"] = "one goal"
    env["QF_READY_SCOPE"] = "tools/qf"
    env["QF_READY_ACCEPTANCE"] = "make verify"
    env["QF_READY_STEPS"] = "init ready do"
    env["QF_READY_STOP"] = "wait"
    res = run(["bash", "tools/qf", "ready", "RUN_ID=run-ready"], cwd=repo, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    ready = repo / "reports" / "run-ready" / "ready.json"
    assert ready.exists()
    assert '"restatement_passed": true' in ready.read_text(encoding="utf-8")


def test_qf_snapshot_appends_conversation_note(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    res = run(
        ["bash", "tools/qf", "snapshot", "RUN_ID=run-snapshot", "NOTE=session checkpoint"],
        cwd=repo,
    )
    assert res.returncode == 0, res.stdout + res.stderr
    snapshot = repo / "reports" / "run-snapshot" / "conversation.md"
    assert snapshot.exists()
    content = snapshot.read_text(encoding="utf-8")
    assert "session checkpoint" in content
    assert "working_tree:" in content
