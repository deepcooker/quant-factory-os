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


def seed_state(repo: Path, run_id: str) -> None:
    (repo / "TASKS" / "TASK-a.md").write_text(
        "\n".join(
            [
                "# TASK: a",
                "",
                f"RUN_ID: {run_id}",
                "",
                "## Goal",
                "Keep flow simple.",
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
        encoding="utf-8",
    )
    (repo / "TASKS" / "STATE.md").write_text(
        "\n".join(
            [
                "# STATE",
                "CURRENT_PROJECT_ID: project-0",
                f"CURRENT_RUN_ID: {run_id}",
                "CURRENT_TASK_FILE: TASKS/TASK-a.md",
                "CURRENT_STATUS: active",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def test_qf_discuss_runs_to_prepare_and_generates_contract_chain(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-execute"
    seed_state(repo, run_id)

    env = os.environ.copy()
    env["QF_READY_REQUIRE_SYNC"] = "0"
    env["QF_READY_GOAL"] = "goal"
    env["QF_READY_SCOPE"] = "scope"
    env["QF_READY_ACCEPTANCE"] = "accept"
    env["QF_READY_STEPS"] = "steps"
    env["QF_READY_STOP"] = "stop"

    ready = run(["bash", "tools/qf", "ready", f"RUN_ID={run_id}"], cwd=repo, env=env)
    assert ready.returncode == 0, ready.stdout + ready.stderr

    orient_file = repo / "SYNC" / "discussion" / run_id / "orient.json"
    orient_obj = json.loads(orient_file.read_text(encoding="utf-8"))
    option = str(orient_obj.get("recommended_option") or "").strip()
    assert option != ""

    choose = run(["bash", "tools/qf", "choose", f"RUN_ID={run_id}", f"OPTION={option}"], cwd=repo)
    assert choose.returncode == 0, choose.stdout + choose.stderr

    discuss = run(["bash", "tools/qf", "discuss", f"RUN_ID={run_id}"], cwd=repo)
    assert discuss.returncode == 0, discuss.stdout + discuss.stderr
    assert "EXECUTE_STATUS: prepared" in discuss.stdout
    assert "EXECUTE_NEXT_COMMAND: tools/qf do queue-next" in discuss.stdout
    assert (repo / "SYNC" / "discussion" / run_id / "council.json").exists()
    assert (repo / "reports" / run_id / "execution_contract.json").exists()
    assert (repo / "reports" / run_id / "slice_state.json").exists()


def test_qf_execute_prints_step_markers_and_json_stream(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-execute-stream"
    seed_state(repo, run_id)

    env = os.environ.copy()
    env["QF_READY_REQUIRE_SYNC"] = "0"
    env["QF_READY_GOAL"] = "goal"
    env["QF_READY_SCOPE"] = "scope"
    env["QF_READY_ACCEPTANCE"] = "accept"
    env["QF_READY_STEPS"] = "steps"
    env["QF_READY_STOP"] = "stop"
    env["QF_EVENT_STREAM"] = "1"

    ready = run(["bash", "tools/qf", "ready", f"RUN_ID={run_id}"], cwd=repo, env=env)
    assert ready.returncode == 0, ready.stdout + ready.stderr

    orient_file = repo / "SYNC" / "discussion" / run_id / "orient.json"
    orient_obj = json.loads(orient_file.read_text(encoding="utf-8"))
    option = str(orient_obj.get("recommended_option") or "").strip()
    assert option != ""
    choose = run(["bash", "tools/qf", "choose", f"RUN_ID={run_id}", f"OPTION={option}"], cwd=repo, env=env)
    assert choose.returncode == 0, choose.stdout + choose.stderr

    execute = run(["bash", "tools/qf", "execute", f"RUN_ID={run_id}", "TARGET=prepare"], cwd=repo, env=env)
    assert execute.returncode == 0, execute.stdout + execute.stderr
    assert "EXECUTE_STEP[1/7]: resolve run and enforce ready gate" in execute.stdout
    assert "EXECUTE_STEP[7/7]: dispatch by target (prepare/do)" in execute.stdout
    assert '"type":"qf_event"' in execute.stdout
    assert '"phase":"execute"' in execute.stdout


def test_qf_execute_do_requires_contract_confirmation(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-execute-confirm"
    seed_state(repo, run_id)

    env = os.environ.copy()
    env["QF_READY_REQUIRE_SYNC"] = "0"
    env["QF_READY_GOAL"] = "goal"
    env["QF_READY_SCOPE"] = "scope"
    env["QF_READY_ACCEPTANCE"] = "accept"
    env["QF_READY_STEPS"] = "steps"
    env["QF_READY_STOP"] = "stop"

    ready = run(["bash", "tools/qf", "ready", f"RUN_ID={run_id}"], cwd=repo, env=env)
    assert ready.returncode == 0, ready.stdout + ready.stderr

    orient_file = repo / "SYNC" / "discussion" / run_id / "orient.json"
    orient_obj = json.loads(orient_file.read_text(encoding="utf-8"))
    option = str(orient_obj.get("recommended_option") or "").strip()
    assert option != ""
    choose = run(["bash", "tools/qf", "choose", f"RUN_ID={run_id}", f"OPTION={option}"], cwd=repo, env=env)
    assert choose.returncode == 0, choose.stdout + choose.stderr

    execute = run(["bash", "tools/qf", "execute", f"RUN_ID={run_id}", "TARGET=do"], cwd=repo, env=env)
    assert execute.returncode != 0
    combined = execute.stdout + execute.stderr
    assert "EXECUTE_NEEDS_CONTRACT_CONFIRM: true" in combined
    assert f"tools/qf execute RUN_ID={run_id} PROJECT_ID=project-0 CONFIRM_CONTRACT=1 TARGET=do" in combined
    assert not (repo / "reports" / run_id / "execution_contract_confirm.json").exists()


def test_qf_execute_prepare_writes_contract_confirmation_when_requested(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-execute-confirm-write"
    seed_state(repo, run_id)

    env = os.environ.copy()
    env["QF_READY_REQUIRE_SYNC"] = "0"
    env["QF_READY_GOAL"] = "goal"
    env["QF_READY_SCOPE"] = "scope"
    env["QF_READY_ACCEPTANCE"] = "accept"
    env["QF_READY_STEPS"] = "steps"
    env["QF_READY_STOP"] = "stop"

    ready = run(["bash", "tools/qf", "ready", f"RUN_ID={run_id}"], cwd=repo, env=env)
    assert ready.returncode == 0, ready.stdout + ready.stderr

    orient_file = repo / "SYNC" / "discussion" / run_id / "orient.json"
    orient_obj = json.loads(orient_file.read_text(encoding="utf-8"))
    option = str(orient_obj.get("recommended_option") or "").strip()
    assert option != ""
    choose = run(["bash", "tools/qf", "choose", f"RUN_ID={run_id}", f"OPTION={option}"], cwd=repo, env=env)
    assert choose.returncode == 0, choose.stdout + choose.stderr

    execute = run(
        ["bash", "tools/qf", "execute", f"RUN_ID={run_id}", "TARGET=prepare", "CONFIRM_CONTRACT=1"],
        cwd=repo,
        env=env,
    )
    assert execute.returncode == 0, execute.stdout + execute.stderr
    confirm_file = repo / "reports" / run_id / "execution_contract_confirm.json"
    assert confirm_file.exists()
    obj = json.loads(confirm_file.read_text(encoding="utf-8"))
    assert obj["project_id"] == "project-0"
    assert obj["run_id"] == run_id
    assert obj["source"] == "manual"
