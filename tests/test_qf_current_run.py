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
    env["QF_READY_REQUIRE_SYNC"] = "0"
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
    env["QF_READY_REQUIRE_SYNC"] = "0"
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
    env["QF_READY_REQUIRE_SYNC"] = "0"
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


def test_qf_resume_uses_merged_pr_lookup_without_create(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)

    checkout_main = run(["git", "checkout", "-b", "main"], cwd=repo)
    assert checkout_main.returncode == 0, checkout_main.stdout + checkout_main.stderr
    (repo / "README.md").write_text("seed\n", encoding="utf-8")
    add_seed = run(["git", "add", "README.md"], cwd=repo)
    assert add_seed.returncode == 0, add_seed.stdout + add_seed.stderr
    seed_commit = run(["git", "commit", "-m", "seed"], cwd=repo)
    assert seed_commit.returncode == 0, seed_commit.stdout + seed_commit.stderr

    origin = tmp_path / "origin.git"
    clone_bare = run(["git", "clone", "--bare", "--no-hardlinks", str(repo), str(origin)], cwd=tmp_path)
    assert clone_bare.returncode == 0, clone_bare.stdout + clone_bare.stderr
    add_remote = run(["git", "remote", "add", "origin", str(origin)], cwd=repo)
    assert add_remote.returncode == 0, add_remote.stdout + add_remote.stderr

    feature_branch = "chore/resume-test"
    write_state(repo, "run-current")
    run_dir = repo / "reports" / "run-current"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "ship_state.json").write_text(
        "\n".join(
            [
                "{",
                '  "run_id": "run-current",',
                f'  "branch": "{feature_branch}",',
                '  "commit": "seed",',
                '  "pr_url": "",',
                '  "step": "branch_prepared",',
                '  "last_error": "",',
                '  "msg": "resume test",',
                '  "updated_at": "2026-02-28T00:00:00+08:00"',
                "}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    bin_dir = repo / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    gh_log = repo / "gh.log"
    (bin_dir / "gh").write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                f"echo \"$*\" >> \"{gh_log}\"",
                "if [[ \"${1:-}\" == \"pr\" && \"${2:-}\" == \"list\" ]]; then",
                "  echo \"https://github.com/example/repo/pull/123\"",
                "  exit 0",
                "fi",
                "if [[ \"${1:-}\" == \"pr\" && \"${2:-}\" == \"create\" ]]; then",
                "  echo \"unexpected pr create\" >&2",
                "  exit 88",
                "fi",
                "if [[ \"${1:-}\" == \"pr\" && \"${2:-}\" == \"view\" ]]; then",
                "  echo \"MERGED\"",
                "  exit 0",
                "fi",
                "if [[ \"${1:-}\" == \"pr\" && \"${2:-}\" == \"merge\" ]]; then",
                "  exit 0",
                "fi",
                "if [[ \"${1:-}\" == \"auth\" && \"${2:-}\" == \"status\" ]]; then",
                "  exit 0",
                "fi",
                "exit 0",
                "",
            ]
        ),
        encoding="utf-8",
    )
    os.chmod(bin_dir / "gh", os.stat(bin_dir / "gh").st_mode | stat.S_IXUSR)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}:{env['PATH']}"
    res = run(["bash", "tools/qf", "resume", "RUN_ID=run-current"], cwd=repo, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "resume done: run-current" in (res.stdout + res.stderr)

    gh_calls = gh_log.read_text(encoding="utf-8")
    assert "pr list" in gh_calls
    assert "pr create" not in gh_calls
