import json
import os
import shutil
import stat
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess:
    merged_env = os.environ.copy()
    merged_env.setdefault("QF_LEARN_MODEL_SYNC", "0")
    if env:
        merged_env.update(env)
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=merged_env,
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
        "docs/CODEX_CLI_OPERATION.md": "# CODEX\n",
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
                "CURRENT_PROJECT_ID: project-0",
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


def write_learn_marker(repo: Path, run_id: str) -> None:
    _ = run_id
    (repo / "reports" / "projects" / "project-0" / "session").mkdir(parents=True, exist_ok=True)
    (repo / "reports" / "projects" / "project-0" / "session" / "learn.json").write_text(
        '{"project_id":"project-0","learn_passed": true, "context_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "context_files": [], "skill_files": [], "exam": {"required": false, "present": false, "passed": false}, "expires_at_utc": "2999-01-01T00:00:00+00:00"}\n',
        encoding="utf-8",
    )


def write_legacy_learn_marker(repo: Path) -> None:
    (repo / "reports" / "session").mkdir(parents=True, exist_ok=True)
    (repo / "reports" / "session" / "learn.json").write_text(
        '{"learn_passed": true, "context_digest": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "context_files": [], "skill_files": [], "exam": {"required": false, "present": false, "passed": false}, "expires_at_utc": "2999-01-01T00:00:00+00:00"}\n',
        encoding="utf-8",
    )


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
    assert obj["project_id"] == "project-0"
    assert obj["sync_passed"] is True
    assert len(obj["files_read"]) >= len(obj["required_files"])
    assert obj["next_command"] == "tools/qf learn"


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
    env["QF_READY_REQUIRE_LEARN"] = "0"

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
    env["QF_READY_REQUIRE_LEARN"] = "0"

    res = run(["bash", "tools/qf", "ready", f"RUN_ID={run_id}"], cwd=repo, env=env)
    assert res.returncode != 0
    combined = res.stdout + res.stderr
    assert "sync gate not satisfied" in combined
    assert f"tools/qf sync RUN_ID={run_id}" in combined


def test_qf_sync_next_command_prefers_choose_when_orient_draft_exists(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)
    write_learn_marker(repo, run_id)
    (repo / "reports" / run_id / "ready.json").write_text(
        '{"run_id":"run-sync","restatement_passed":true,"sync_gate":{"required":false,"sync_passed":true,"sync_report_file":""}}\n',
        encoding="utf-8",
    )
    orient_dir = repo / "SYNC" / "discussion" / run_id
    orient_dir.mkdir(parents=True, exist_ok=True)
    (orient_dir / "orient.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "recommended_option": "ready-strong-brief",
                "directions": [{"id": "ready-strong-brief"}],
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    res = run(["bash", "tools/qf", "sync", f"RUN_ID={run_id}"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    report_file = repo / "reports" / run_id / "sync_report.json"
    obj = json.loads(report_file.read_text(encoding="utf-8"))
    assert obj["next_command"] == f"tools/qf choose RUN_ID={run_id} OPTION=ready-strong-brief"


def test_qf_sync_next_command_prefers_council_after_choose(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)
    write_learn_marker(repo, run_id)
    run_dir = repo / "reports" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "ready.json").write_text(
        '{"run_id":"run-sync","restatement_passed":true,"sync_gate":{"required":false,"sync_passed":true,"sync_report_file":""}}\n',
        encoding="utf-8",
    )
    (run_dir / "orient_choice.json").write_text(
        '{"run_id":"run-sync","selected_option":"ready-strong-brief","discussion_confirmed":true}\n',
        encoding="utf-8",
    )

    res = run(["bash", "tools/qf", "sync", f"RUN_ID={run_id}"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    obj = json.loads((repo / "reports" / run_id / "sync_report.json").read_text(encoding="utf-8"))
    assert obj["next_command"] == f"tools/qf council RUN_ID={run_id}"


def test_qf_sync_next_command_prefers_arbiter_then_slice_then_do(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)
    write_learn_marker(repo, run_id)
    run_dir = repo / "reports" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    discussion_dir = repo / "SYNC" / "discussion" / run_id
    discussion_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "ready.json").write_text(
        '{"run_id":"run-sync","restatement_passed":true,"sync_gate":{"required":false,"sync_passed":true,"sync_report_file":""}}\n',
        encoding="utf-8",
    )
    (run_dir / "orient_choice.json").write_text(
        '{"run_id":"run-sync","selected_option":"ready-strong-brief","discussion_confirmed":true}\n',
        encoding="utf-8",
    )
    (discussion_dir / "council.json").write_text('{"run_id":"run-sync","roles":[]}\n', encoding="utf-8")

    res1 = run(["bash", "tools/qf", "sync", f"RUN_ID={run_id}"], cwd=repo)
    assert res1.returncode == 0, res1.stdout + res1.stderr
    obj1 = json.loads((repo / "reports" / run_id / "sync_report.json").read_text(encoding="utf-8"))
    assert obj1["next_command"] == f"tools/qf arbiter RUN_ID={run_id}"

    (run_dir / "execution_contract.json").write_text('{"run_id":"run-sync","tasks":[]}\n', encoding="utf-8")
    res2 = run(["bash", "tools/qf", "sync", f"RUN_ID={run_id}"], cwd=repo)
    assert res2.returncode == 0, res2.stdout + res2.stderr
    obj2 = json.loads((repo / "reports" / run_id / "sync_report.json").read_text(encoding="utf-8"))
    assert obj2["next_command"] == f"tools/qf slice RUN_ID={run_id}"

    (run_dir / "slice_state.json").write_text('{"run_id":"run-sync","tasks_total":0}\n', encoding="utf-8")
    res3 = run(["bash", "tools/qf", "sync", f"RUN_ID={run_id}"], cwd=repo)
    assert res3.returncode == 0, res3.stdout + res3.stderr
    obj3 = json.loads((repo / "reports" / run_id / "sync_report.json").read_text(encoding="utf-8"))
    assert obj3["next_command"] == "tools/qf do queue-next"


def test_qf_learn_generates_report_and_step_markers(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)

    res = run(["bash", "tools/qf", "learn", f"RUN_ID={run_id}", "REQUIRE_EXAM=0"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "LEARN_STEP[1/8]: resolve run context" in res.stdout
    assert "LEARN_STEP[8/8]: print learn artifacts" in res.stdout
    learn_file = repo / "reports" / "projects" / "project-0" / "session" / "learn.json"
    assert learn_file.exists()
    obj = json.loads(learn_file.read_text(encoding="utf-8"))
    assert obj["learn_passed"] is True
    assert obj["project_id"] == "project-0"
    assert obj.get("scope") == "session"


def test_qf_learn_accepts_model_sync_arg_without_run_id_conflict(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)

    res = run(
        ["bash", "tools/qf", "learn", f"RUN_ID={run_id}", "REQUIRE_EXAM=0", "MODEL_SYNC=0"],
        cwd=repo,
    )
    assert res.returncode == 0, res.stdout + res.stderr
    combined = res.stdout + res.stderr
    assert "run-id mismatch" not in combined
    assert "LEARN_MODEL_SYNC_MODE:" not in combined


def test_qf_learn_session_mode_without_run_context(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)
    (repo / "TASKS" / "STATE.md").write_text(
        "\n".join(
            [
                "# STATE",
                "CURRENT_PROJECT_ID: project-0",
                "CURRENT_RUN_ID:",
                "CURRENT_TASK_FILE: TASKS/TASK-auto.md",
                "CURRENT_STATUS: active",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    res = run(["bash", "tools/qf", "learn", "REQUIRE_EXAM=0"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "LEARN_CONTEXT_RUN_ID: (none)" in res.stdout
    assert "LEARN_SYNC_MODE: session-direct-read" in res.stdout

    learn_file = repo / "reports" / "projects" / "project-0" / "session" / "learn.json"
    obj = json.loads(learn_file.read_text(encoding="utf-8"))
    assert obj["project_id"] == "project-0"
    assert obj["context_run_id"] == ""
    assert obj["sync"]["mode"] == "direct-read"
    assert obj["learn_passed"] is True


def test_qf_learn_session_mode_bypasses_exam_without_run_context(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)
    (repo / "TASKS" / "STATE.md").write_text(
        "\n".join(
            [
                "# STATE",
                "CURRENT_PROJECT_ID: project-0",
                "CURRENT_RUN_ID:",
                "CURRENT_TASK_FILE: TASKS/TASK-auto.md",
                "CURRENT_STATUS: active",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    res = run(["bash", "tools/qf", "learn"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "LEARN_EXAM_BYPASS_NO_RUN_CONTEXT: true" in res.stdout

    learn_file = repo / "reports" / "projects" / "project-0" / "session" / "learn.json"
    obj = json.loads(learn_file.read_text(encoding="utf-8"))
    assert obj["project_id"] == "project-0"
    assert obj["exam"]["required"] is False
    assert obj["learn_passed"] is True


def test_qf_ready_requires_learn_when_enabled_and_auto_disabled(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)

    env = os.environ.copy()
    env["QF_READY_REQUIRE_SYNC"] = "0"
    env["QF_READY_REQUIRE_LEARN"] = "1"
    env["QF_READY_AUTO_LEARN"] = "0"
    env["QF_READY_GOAL"] = "goal"
    env["QF_READY_SCOPE"] = "scope"
    env["QF_READY_ACCEPTANCE"] = "accept"
    env["QF_READY_STEPS"] = "steps"
    env["QF_READY_STOP"] = "stop"

    res = run(["bash", "tools/qf", "ready", "RUN_ID=run-ready"], cwd=repo, env=env)
    assert res.returncode != 0
    combined = res.stdout + res.stderr
    assert "learn gate not satisfied" in combined
    assert "tools/qf learn" in combined


def test_qf_ready_auto_runs_learn_when_missing(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)

    env = os.environ.copy()
    env["QF_READY_GOAL"] = "goal"
    env["QF_READY_SCOPE"] = "scope"
    env["QF_READY_ACCEPTANCE"] = "accept"
    env["QF_READY_STEPS"] = "steps"
    env["QF_READY_STOP"] = "stop"
    env["QF_LEARN_REQUIRE_EXAM"] = "0"

    res = run(["bash", "tools/qf", "ready", f"RUN_ID={run_id}"], cwd=repo, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "LEARN_AUTO_RUN: tools/qf learn" in res.stdout
    assert (repo / "reports" / "projects" / "project-0" / "session" / "learn.json").exists()
    assert (repo / "reports" / run_id / "ready.json").exists()


def test_qf_ready_legacy_learn_marker_is_compatible_for_project0(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)
    write_legacy_learn_marker(repo)

    env = os.environ.copy()
    env["QF_READY_REQUIRE_SYNC"] = "0"
    env["QF_READY_REQUIRE_LEARN"] = "1"
    env["QF_READY_AUTO_LEARN"] = "0"
    env["QF_READY_GOAL"] = "goal"
    env["QF_READY_SCOPE"] = "scope"
    env["QF_READY_ACCEPTANCE"] = "accept"
    env["QF_READY_STEPS"] = "steps"
    env["QF_READY_STOP"] = "stop"

    res = run(["bash", "tools/qf", "ready", f"RUN_ID={run_id}"], cwd=repo, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "READY_LEARN_REPORT: reports/session/learn.json" in res.stdout


def test_qf_learn_log_flag_writes_stdout_log(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-sync"
    seed_sync_required_files(repo, run_id)

    res = run(["bash", "tools/qf", "learn", f"RUN_ID={run_id}", "REQUIRE_EXAM=0", "-log"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "LEARN_LOG_FILE: reports/projects/project-0/session/learn.stdout.log" in res.stdout
    log_file = repo / "reports" / "projects" / "project-0" / "session" / "learn.stdout.log"
    assert log_file.exists()
    content = log_file.read_text(encoding="utf-8")
    assert "LEARN_STEP[1/8]: resolve run context" in content
    assert "LEARN_STATUS: pass" in content
