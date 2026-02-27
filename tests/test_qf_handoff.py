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


def test_qf_handoff_generates_summary_with_existing_artifacts(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-handoff"
    out_dir = repo / "reports" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    ready = {
        "run_id": run_id,
        "restatement_passed": True,
        "restatement": {
            "goal": "g",
            "scope": "s",
            "acceptance": "a",
            "steps": "st",
            "stop_condition": "stop",
        },
    }
    (out_dir / "ready.json").write_text(json.dumps(ready, ensure_ascii=False), encoding="utf-8")
    (out_dir / "conversation.md").write_text("## t1\n- note: checkpoint\n", encoding="utf-8")
    (out_dir / "execution.jsonl").write_text(
        json.dumps(
            {
                "ts": "2026-02-27T00:00:00+00:00",
                "phase": "do",
                "action": "do_pick_success",
                "status": "ok",
                "artifacts": "TASK_FILE=TASKS/TASK-a.md",
            },
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (out_dir / "ship_state.json").write_text(
        json.dumps({"step": "pr_merge", "pr_url": "https://example/pr/1", "branch": "x"}, ensure_ascii=False),
        encoding="utf-8",
    )

    res = run(["bash", "tools/qf", "handoff", f"RUN_ID={run_id}"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    handoff = (out_dir / "handoff.md").read_text(encoding="utf-8")
    assert "Session Handoff" in handoff
    assert "Recent Execution Events" in handoff
    assert "do/do_pick_success" in handoff
    assert "tools/qf ready" in handoff


def test_qf_handoff_handles_missing_inputs(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    run_id = "run-missing-handoff"
    (repo / "reports" / run_id).mkdir(parents=True, exist_ok=True)

    res = run(["bash", "tools/qf", "handoff", f"RUN_ID={run_id}"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    handoff = (repo / "reports" / run_id / "handoff.md").read_text(encoding="utf-8")
    assert "missing: ready.json" in handoff
    assert "missing: execution.jsonl" in handoff


def test_qf_init_prints_handoff_hint_for_recent_run(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    (repo / "tools" / "doctor.sh").write_text("#!/usr/bin/env bash\nset -euo pipefail\necho doctor-ok\n", encoding="utf-8")
    os.chmod(repo / "tools" / "doctor.sh", os.stat(repo / "tools" / "doctor.sh").st_mode | stat.S_IXUSR)
    (repo / "TASKS" / "STATE.md").write_text("# state\n", encoding="utf-8")
    (repo / "TASKS" / "QUEUE.md").write_text("# queue\n", encoding="utf-8")
    old = repo / "reports" / "run-prev"
    old.mkdir(parents=True, exist_ok=True)
    (old / "execution.jsonl").write_text('{"ts":"2026-02-27T00:00:00+00:00","run_id":"run-prev"}\n', encoding="utf-8")

    run(["git", "add", "."], cwd=repo)
    run(["git", "commit", "-m", "seed"], cwd=repo)

    env = os.environ.copy()
    env["QF_SKIP_SYNC"] = "1"
    res = run(["bash", "tools/qf", "init"], cwd=repo, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "tools/qf handoff RUN_ID=run-prev" in res.stdout
