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


def test_qf_plan_keeps_worktree_clean_and_cleans_pick_candidate(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    repo = tmp_path / "repo"
    tools_dir = repo / "tools"
    tasks_dir = repo / "TASKS"
    reports_dir = repo / "reports"

    tools_dir.mkdir(parents=True)
    tasks_dir.mkdir(parents=True)
    reports_dir.mkdir(parents=True)

    shutil.copy2(repo_root / "tools" / "qf", tools_dir / "qf")
    mode = os.stat(tools_dir / "qf").st_mode
    os.chmod(tools_dir / "qf", mode | stat.S_IXUSR)

    (tools_dir / "task.sh").write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "mkdir -p TASKS reports/run-2026-02-26-pick-candidate",
                "printf '# TODO Proposal\\nnew\\n' > TASKS/TODO_PROPOSAL.md",
                "printf 'tmp\\n' > reports/run-2026-02-26-pick-candidate/candidate.txt",
                "echo 'PROPOSAL_FILE: TASKS/TODO_PROPOSAL.md'",
            ]
        ),
        encoding="utf-8",
    )
    mode = os.stat(tools_dir / "task.sh").st_mode
    os.chmod(tools_dir / "task.sh", mode | stat.S_IXUSR)

    (tasks_dir / "TODO_PROPOSAL.md").write_text("# TODO Proposal\nbaseline\n", encoding="utf-8")

    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test User"], cwd=repo)
    run(["git", "add", "."], cwd=repo)
    commit = run(["git", "commit", "-m", "init"], cwd=repo)
    assert commit.returncode == 0, commit.stdout + commit.stderr

    env = os.environ.copy()
    env["QF_SKIP_SYNC"] = "1"
    res = run(["bash", "tools/qf", "plan", "20"], cwd=repo, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "PROPOSAL_COPY:" in res.stdout
    assert "CLEANED: reports/run-2026-02-26-pick-candidate" in res.stdout

    status = run(["git", "status", "--porcelain"], cwd=repo)
    assert status.returncode == 0, status.stdout + status.stderr
    assert status.stdout.strip() == ""
    assert not any(reports_dir.glob("run-*-pick-candidate"))


def test_qf_plan_auto_stashes_dirty_worktree(tmp_path: Path):
    repo_root = Path(__file__).resolve().parents[1]
    repo = tmp_path / "repo"
    tools_dir = repo / "tools"
    tasks_dir = repo / "TASKS"

    tools_dir.mkdir(parents=True)
    tasks_dir.mkdir(parents=True)

    shutil.copy2(repo_root / "tools" / "qf", tools_dir / "qf")
    mode = os.stat(tools_dir / "qf").st_mode
    os.chmod(tools_dir / "qf", mode | stat.S_IXUSR)

    (tools_dir / "task.sh").write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "mkdir -p TASKS",
                "printf '# TODO Proposal\\nauto\\n' > TASKS/TODO_PROPOSAL.md",
                "echo 'PROPOSAL_FILE: TASKS/TODO_PROPOSAL.md'",
            ]
        ),
        encoding="utf-8",
    )
    mode = os.stat(tools_dir / "task.sh").st_mode
    os.chmod(tools_dir / "task.sh", mode | stat.S_IXUSR)

    (repo / "README.md").write_text("seed\n", encoding="utf-8")

    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test User"], cwd=repo)
    run(["git", "add", "."], cwd=repo)
    commit = run(["git", "commit", "-m", "init"], cwd=repo)
    assert commit.returncode == 0, commit.stdout + commit.stderr

    (repo / "README.md").write_text("seed\nchanged\n", encoding="utf-8")

    env = os.environ.copy()
    env["QF_SKIP_SYNC"] = "1"
    res = run(["bash", "tools/qf", "plan", "20"], cwd=repo, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "Detected local changes. Stashing as:" in res.stdout

    status = run(["git", "status", "--porcelain"], cwd=repo)
    assert status.returncode == 0, status.stdout + status.stderr
    assert status.stdout.strip() == ""
