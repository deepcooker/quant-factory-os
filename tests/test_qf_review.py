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


def write_state(repo: Path, run_id: str, status: str = "active") -> None:
    (repo / "TASKS" / "STATE.md").write_text(
        "\n".join(
            [
                "# STATE",
                f"CURRENT_RUN_ID: {run_id}",
                "CURRENT_TASK_FILE: TASKS/TASK-a.md",
                f"CURRENT_STATUS: {status}",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (repo / "TASKS" / "TASK-a.md").write_text("# TASK: a\n", encoding="utf-8")


def test_qf_review_generates_drift_reports(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-review"
    write_state(repo, run_id, status="active")

    run_dir = repo / "reports" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "summary.md").write_text(
        "\n".join(
            [
                "# Summary",
                "",
                "## Commands / Outputs",
                "- make verify",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    (run_dir / "decision.md").write_text(
        "\n".join(
            [
                "# Decision",
                "",
                "## Stop Reason",
                "- task_done",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    res = run(["bash", "tools/qf", "review", f"RUN_ID={run_id}", "AUTO_FIX=0"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "REVIEW_STATUS: pass" in res.stdout
    assert (run_dir / "drift_review.json").exists()
    assert (run_dir / "drift_review.md").exists()


def test_qf_review_strict_blocks_without_verify_record(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-review"
    write_state(repo, run_id, status="done")

    run_dir = repo / "reports" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "summary.md").write_text("# Summary\n\nno verify\n", encoding="utf-8")
    (run_dir / "decision.md").write_text("# Decision\n\n## Stop Reason\n- task_done\n", encoding="utf-8")
    (run_dir / "orient_choice.json").write_text("{}", encoding="utf-8")
    (run_dir / "direction_contract.json").write_text("{}", encoding="utf-8")

    res = run(
        ["bash", "tools/qf", "review", f"RUN_ID={run_id}", "STRICT=1", "AUTO_FIX=0"],
        cwd=repo,
    )
    assert res.returncode != 0
    combined = res.stdout + res.stderr
    assert "REVIEW_STATUS: fail" in combined
    assert "REVIEW_BLOCKERS:" in combined


def test_qf_review_strict_autofix_unblocks(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-review"
    write_state(repo, run_id, status="done")

    run_dir = repo / "reports" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "summary.md").write_text("# Summary\n\n", encoding="utf-8")
    (run_dir / "decision.md").write_text("# Decision\n\n", encoding="utf-8")
    (run_dir / "orient_choice.json").write_text("{}", encoding="utf-8")
    (run_dir / "direction_contract.json").write_text("{}", encoding="utf-8")

    res = run(
        ["bash", "tools/qf", "review", f"RUN_ID={run_id}", "STRICT=1", "AUTO_FIX=1"],
        cwd=repo,
    )
    assert res.returncode == 0, res.stdout + res.stderr
    assert "REVIEW_STATUS: pass" in res.stdout
    summary = (run_dir / "summary.md").read_text(encoding="utf-8")
    assert "make verify" in summary.lower()

    obj = json.loads((run_dir / "drift_review.json").read_text(encoding="utf-8"))
    assert obj["status"] == "pass"
    assert obj["auto_fix"] is True
