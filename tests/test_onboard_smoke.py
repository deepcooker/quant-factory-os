import os
import subprocess
from pathlib import Path


def test_onboard_outputs_required_entrypoints_and_writes_file(tmp_path: Path):
    run_id = "run-2026-02-24-session-onboard-after-ship-next"
    repo_root = tmp_path

    (repo_root / "TASKS").mkdir(parents=True)
    (repo_root / "reports" / "run-a").mkdir(parents=True)
    (repo_root / "reports" / "run-b").mkdir(parents=True)
    (repo_root / "TASKS" / "STATE.md").write_text("# STATE\n", encoding="utf-8")
    (repo_root / "TASKS" / "QUEUE.md").write_text("# QUEUE\n\n## Queue\n", encoding="utf-8")
    (repo_root / "reports" / "run-a" / "decision.md").write_text("# Decision A\n", encoding="utf-8")
    (repo_root / "reports" / "run-b" / "decision.md").write_text("# Decision B\n", encoding="utf-8")

    env = os.environ.copy()
    env["ONBOARD_REPO_ROOT"] = str(repo_root)
    env["ONBOARD_REPORTS_DIR"] = str(repo_root / "reports")
    env["ONBOARD_OUT_DIR"] = str(repo_root / "reports" / run_id)
    env["ONBOARD_STATE_FILE"] = str(repo_root / "TASKS" / "STATE.md")
    env["ONBOARD_QUEUE_FILE"] = str(repo_root / "TASKS" / "QUEUE.md")
    env["ONBOARD_DECISIONS_GLOB"] = str(repo_root / "reports" / "run-*" / "decision.md")

    res = subprocess.run(
        ["bash", "tools/onboard.sh", run_id],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert res.returncode == 0, res.stdout + res.stderr

    combined = res.stdout + res.stderr
    assert "AGENTS.md" in combined
    assert "PROJECT_GUIDE.md" in combined
    assert "docs/WORKFLOW.md" in combined
    assert "TASKS/STATE.md" in combined
    assert "TASKS/QUEUE.md" in combined
    assert "强制复述模板入口" in combined
    assert "最近 decision 入口列表" in combined
    assert "reports/run-a/decision.md" in combined or "reports/run-b/decision.md" in combined

    onboard_file = repo_root / "reports" / run_id / "onboard.md"
    assert onboard_file.exists()
