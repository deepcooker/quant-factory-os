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


def seed_sync_required_files(repo: Path, run_id: str) -> None:
    files = {
        "README.md": "# quant-factory-os\n\nquant-factory-os is the governance/execution base for quant engineering.\n",
        "SYNC/README.md": "# sync\n",
        "SYNC/READ_ORDER.md": "# read order\n",
        "SYNC/CURRENT_STATE.md": "# current\n",
        "SYNC/SESSION_LATEST.md": "# latest\n",
        "SYNC/DECISIONS_LATEST.md": "# decisions\n",
        "SYNC/LINKS.md": "# links\n",
        "SYNC/EXAM_PLAN_PROMPT.md": "# prompt\n",
        "SYNC/EXAM_ANSWER_TEMPLATE.md": "# template\n",
        "SYNC/EXAM_WORKFLOW.md": "# workflow\n",
        "SYNC/EXAM_RUBRIC.json": "{}\n",
        "AGENTS.md": "# AGENTS\n",
        "docs/WORKFLOW.md": "# WORKFLOW\n",
        "docs/ENTITIES.md": "# ENTITIES\n",
        "docs/PROJECT_GUIDE.md": "## 0. 一句话北极星（你最终要什么）\n系统目标是自动化 -> 自我迭代 -> 涌现智能。\n",
        "TASKS/QUEUE.md": "# QUEUE\n",
        "TASKS/TASK-auto.md": "\n".join(
            [
                "# TASK: auto",
                "",
                f"RUN_ID: {run_id}",
                "",
                "## Goal",
                "Keep sync and ready automated.",
                "",
                "## Scope (Required)",
                "- `tools/qf`",
                "",
                "## Acceptance",
                "- [ ] make verify",
                "",
            ]
        )
        + "\n",
        "TASKS/STATE.md": "\n".join(
            [
                "# STATE",
                f"CURRENT_RUN_ID: {run_id}",
                "CURRENT_TASK_FILE: TASKS/TASK-auto.md",
                "CURRENT_STATUS: active",
                "",
            ]
        )
        + "\n",
    }

    for rel, content in files.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    run_dir = repo / "reports" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "decision.md").write_text("# Decision\n", encoding="utf-8")
    (run_dir / "summary.md").write_text("# Summary\n", encoding="utf-8")


def test_qf_sync_writes_sync_report_files(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)

    res = run(["bash", "tools/qf", "sync", f"RUN_ID={run_id}"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "SYNC_PASS: true" in res.stdout
    assert "SYNC_REPORT_FILE:" in res.stdout

    report_file = repo / "reports" / run_id / "sync_report.json"
    report_md = repo / "reports" / run_id / "sync_report.md"
    assert report_file.exists()
    assert report_md.exists()

    obj = json.loads(report_file.read_text(encoding="utf-8"))
    assert obj["sync_passed"] is True
    assert len(obj["files_read"]) >= len(obj["required_files"])
    assert obj["next_command"] == "tools/qf ready"


def test_qf_ready_auto_runs_sync_when_missing(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)

    env = os.environ.copy()
    env["QF_READY_GOAL"] = "goal"
    env["QF_READY_SCOPE"] = "scope"
    env["QF_READY_ACCEPTANCE"] = "accept"
    env["QF_READY_STEPS"] = "steps"
    env["QF_READY_STOP"] = "stop"

    res = run(["bash", "tools/qf", "ready", f"RUN_ID={run_id}"], cwd=repo, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "SYNC_AUTO_RUN: tools/qf sync RUN_ID=run-sync" in res.stdout
    assert (repo / "reports" / run_id / "sync_report.json").exists()
    assert (repo / "reports" / run_id / "ready.json").exists()


def test_qf_ready_fails_without_sync_when_auto_sync_disabled(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)

    env = os.environ.copy()
    env["QF_READY_GOAL"] = "goal"
    env["QF_READY_SCOPE"] = "scope"
    env["QF_READY_ACCEPTANCE"] = "accept"
    env["QF_READY_STEPS"] = "steps"
    env["QF_READY_STOP"] = "stop"
    env["QF_READY_AUTO_SYNC"] = "0"

    res = run(["bash", "tools/qf", "ready", f"RUN_ID={run_id}"], cwd=repo, env=env)
    assert res.returncode != 0
    combined = res.stdout + res.stderr
    assert "sync gate not satisfied" in combined
    assert f"tools/qf sync RUN_ID={run_id}" in combined
