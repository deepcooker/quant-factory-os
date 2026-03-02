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
    (repo / "docs").mkdir(parents=True)
    (repo / "SYNC").mkdir(parents=True)

    shutil.copy2(repo_root / "tools" / "qf", repo / "tools" / "qf")
    mode = os.stat(repo / "tools" / "qf").st_mode
    os.chmod(repo / "tools" / "qf", mode | stat.S_IXUSR)

    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test User"], cwd=repo)
    return repo


def seed_docs(repo: Path, run_id: str) -> None:
    files = {
        "README.md": "# quant-factory-os\n\nquant-factory-os is the governance/execution base for quant engineering.\n",
        "AGENTS.md": "# AGENTS\n",
        "docs/PROJECT_GUIDE.md": "## 0. 一句话北极星（你最终要什么）\n目标是自动化 -> 自我迭代 -> 涌现智能。\n",
        "docs/WORKFLOW.md": "# WORKFLOW\nPlanner Reviewer Observer\n",
        "docs/ENTITIES.md": "# ENTITIES\n",
        "TASKS/QUEUE.md": "# QUEUE\n- [x] done item\n",
        "TASKS/STATE.md": "\n".join(
            [
                "# STATE",
                f"CURRENT_RUN_ID: {run_id}",
                "CURRENT_TASK_FILE: TASKS/TASK-a.md",
                "CURRENT_STATUS: active",
                "",
            ]
        )
        + "\n",
        "TASKS/TASK-a.md": "# TASK: a\n",
        "SYNC/README.md": "# sync\n",
        "SYNC/READ_ORDER.md": "# order\n",
        "SYNC/CURRENT_STATE.md": "# current\n",
        "SYNC/SESSION_LATEST.md": "# latest\n",
        "SYNC/DECISIONS_LATEST.md": "# decisions\n",
        "SYNC/LINKS.md": "# links\n",
        "SYNC/EXAM_PLAN_PROMPT.md": "# prompt\n",
        "SYNC/EXAM_ANSWER_TEMPLATE.md": "# template\n",
        "SYNC/EXAM_WORKFLOW.md": "# workflow\n",
        "SYNC/EXAM_RUBRIC.json": "{}\n",
    }
    for rel, content in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")

    run_dir = repo / "reports" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "summary.md").write_text("# Summary\n", encoding="utf-8")
    (run_dir / "decision.md").write_text("# Decision\n", encoding="utf-8")
    (run_dir / "ready.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "restatement_passed": True,
                "sync_gate": {
                    "required": False,
                    "sync_passed": True,
                    "sync_report_file": "",
                },
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def commit_all(repo: Path, msg: str) -> None:
    add = run(["git", "add", "."], cwd=repo)
    assert add.returncode == 0, add.stdout + add.stderr
    commit = run(["git", "commit", "-m", msg], cwd=repo)
    assert commit.returncode == 0, commit.stdout + commit.stderr


def test_qf_orient_and_choose_write_reports(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-current"
    seed_docs(repo, run_id)
    commit_all(repo, "seed")

    orient = run(["bash", "tools/qf", "orient", f"RUN_ID={run_id}"], cwd=repo)
    assert orient.returncode == 0, orient.stdout + orient.stderr
    assert "ORIENT_OPTIONS:" in orient.stdout
    orient_file = repo / "reports" / run_id / "orient.json"
    assert orient_file.exists()
    orient_obj = json.loads(orient_file.read_text(encoding="utf-8"))
    assert len(orient_obj.get("directions", [])) >= 3
    recommended = orient_obj.get("recommended_option", "")
    assert recommended

    choose = run(["bash", "tools/qf", "choose", f"RUN_ID={run_id}", f"OPTION={recommended}"], cwd=repo)
    assert choose.returncode == 0, choose.stdout + choose.stderr
    assert f"CHOOSE_OPTION: {recommended}" in choose.stdout
    choice_file = repo / "reports" / run_id / "orient_choice.json"
    assert choice_file.exists()


def test_qf_do_autoplan_then_pick_success(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-current"
    seed_docs(repo, run_id)

    task_script = repo / "tools" / "task.sh"
    task_script.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "if [[ \"${1:-}\" == \"--plan\" ]]; then",
                "  mkdir -p TASKS",
                "  printf '# TODO Proposal\\n' > TASKS/TODO_PROPOSAL.md",
                "  echo 'PROPOSAL_FILE: TASKS/TODO_PROPOSAL.md'",
                "  exit 0",
                "fi",
                "if [[ \"${1:-}\" == \"--pick\" && \"${2:-}\" == \"queue-next\" ]]; then",
                "  if [[ ! -f TASKS/TODO_PROPOSAL.md ]]; then",
                "    echo '❌ 未找到 proposal：TASKS/TODO_PROPOSAL.md' >&2",
                "    exit 1",
                "  fi",
                "  echo 'TASK_FILE: TASKS/TASK-picked.md'",
                "  echo 'RUN_ID: run-picked'",
                "  echo 'EVIDENCE_PATH: reports/run-picked/'",
                "  exit 0",
                "fi",
                "exit 1",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    os.chmod(task_script, os.stat(task_script).st_mode | stat.S_IXUSR)
    commit_all(repo, "seed")

    env = os.environ.copy()
    env["QF_SKIP_SYNC"] = "1"
    env["QF_READY_REQUIRE_SYNC"] = "0"
    res = run(["bash", "tools/qf", "do", "queue-next"], cwd=repo, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "TASK_FILE: TASKS/TASK-picked.md" in res.stdout
    assert not (repo / "TASKS" / "TODO_PROPOSAL.md").exists()


def test_qf_do_queue_empty_shows_orient_hint(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-current"
    seed_docs(repo, run_id)

    task_script = repo / "tools" / "task.sh"
    task_script.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "if [[ \"${1:-}\" == \"--plan\" ]]; then",
                "  printf '# TODO Proposal\\n' > TASKS/TODO_PROPOSAL.md",
                "  echo 'PROPOSAL_FILE: TASKS/TODO_PROPOSAL.md'",
                "  exit 0",
                "fi",
                "if [[ \"${1:-}\" == \"--pick\" && \"${2:-}\" == \"queue-next\" ]]; then",
                "  echo '❌ QUEUE 中没有未完成项（- [ ]）' >&2",
                "  exit 1",
                "fi",
                "exit 1",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    os.chmod(task_script, os.stat(task_script).st_mode | stat.S_IXUSR)
    commit_all(repo, "seed")

    env = os.environ.copy()
    env["QF_SKIP_SYNC"] = "1"
    env["QF_READY_REQUIRE_SYNC"] = "0"
    res = run(["bash", "tools/qf", "do", "queue-next"], cwd=repo, env=env)
    assert res.returncode != 0
    combined = res.stdout + res.stderr
    assert "下一步建议：tools/qf orient RUN_ID=run-current" in combined


def test_qf_do_sync_before_execution_log_write(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-current"
    seed_docs(repo, run_id)

    (repo / "reports" / run_id / "execution.jsonl").write_text('{"seed":"1"}\n', encoding="utf-8")
    (repo / "TASKS" / "TODO_PROPOSAL.md").write_text("# TODO Proposal\n", encoding="utf-8")

    task_script = repo / "tools" / "task.sh"
    task_script.write_text(
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "if [[ \"${1:-}\" == \"--pick\" && \"${2:-}\" == \"queue-next\" ]]; then",
                "  echo 'TASK_FILE: TASKS/TASK-picked.md'",
                "  echo 'RUN_ID: run-picked'",
                "  echo 'EVIDENCE_PATH: reports/run-picked/'",
                "  exit 0",
                "fi",
                "exit 1",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    os.chmod(task_script, os.stat(task_script).st_mode | stat.S_IXUSR)

    checkout_main = run(["git", "checkout", "-b", "main"], cwd=repo)
    assert checkout_main.returncode == 0, checkout_main.stdout + checkout_main.stderr
    commit_all(repo, "seed")

    origin = tmp_path / "origin.git"
    clone_bare = run(["git", "clone", "--bare", "--no-hardlinks", str(repo), str(origin)], cwd=tmp_path)
    assert clone_bare.returncode == 0, clone_bare.stdout + clone_bare.stderr
    add_remote = run(["git", "remote", "add", "origin", str(origin)], cwd=repo)
    assert add_remote.returncode == 0, add_remote.stdout + add_remote.stderr

    env = os.environ.copy()
    env["QF_READY_REQUIRE_SYNC"] = "0"
    res = run(["bash", "tools/qf", "do", "queue-next"], cwd=repo, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "TASK_FILE: TASKS/TASK-picked.md" in res.stdout
