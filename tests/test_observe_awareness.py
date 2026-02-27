import os
import subprocess
from datetime import date
from pathlib import Path


def _run_observe(tmp_path: Path, run_id: str):
    env = os.environ.copy()
    env["AWARENESS_REPO_ROOT"] = str(tmp_path)
    env["AWARENESS_REPORTS_DIR"] = str(tmp_path / "reports")
    env["AWARENESS_STATE_FILE"] = str(tmp_path / "TASKS" / "STATE.md")
    env["AWARENESS_QUEUE_FILE"] = str(tmp_path / "TASKS" / "QUEUE.md")
    env["AWARENESS_MISTAKES_DIR"] = str(tmp_path / "MISTAKES")
    env["AWARENESS_OUT_DIR"] = str(tmp_path / "reports" / run_id)
    return subprocess.run(
        ["bash", "tools/observe.sh", run_id],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        text=True,
        capture_output=True,
    )


def test_awareness_happy_path(tmp_path: Path):
    run_id = "run-2026-02-24-observer-awareness-digest"
    today = date.today().strftime("%Y-%m-%d")
    shipped_run = f"run-{today}-sample-ship"

    (tmp_path / "reports" / shipped_run).mkdir(parents=True)
    (tmp_path / "reports" / shipped_run / "decision.md").write_text("# Decision\n", encoding="utf-8")
    (tmp_path / "reports" / shipped_run / "summary.md").write_text("# Summary\n", encoding="utf-8")
    (tmp_path / "reports" / shipped_run / "mistake_log.jsonl").write_text(
        '{"ts":"2026-02-27T00:00:00Z","run_id":"run-x","category":"execution_error","step":"pr_merge","source":"retry","error":"merge blocked"}\n',
        encoding="utf-8",
    )

    (tmp_path / "TASKS").mkdir(parents=True)
    (tmp_path / "TASKS" / "STATE.md").write_text("## Risks\n- backlog drift\n", encoding="utf-8")
    (tmp_path / "TASKS" / "QUEUE.md").write_text(
        "\n".join(
            [
                "# QUEUE",
                "",
                "## Queue",
                "- [ ] TODO Title: improve observer confidence",
            ]
        ),
        encoding="utf-8",
    )

    (tmp_path / "MISTAKES").mkdir(parents=True)
    (tmp_path / "MISTAKES" / "a.md").write_text("symptom: flaky ci\n", encoding="utf-8")
    (tmp_path / "MISTAKES" / "b.md").write_text("symptom: flaky ci\n", encoding="utf-8")

    res = _run_observe(tmp_path, run_id)
    assert res.returncode == 0, res.stdout + res.stderr

    out = (tmp_path / "reports" / run_id / "awareness.md").read_text(encoding="utf-8")
    assert "## 本周 shipped runs" in out
    assert shipped_run in out
    assert "## 重复失败模式" in out
    assert "flaky ci" in out
    assert "## 当前风险" in out
    assert "backlog drift" in out
    assert "## 下一枪建议" in out
    assert "TASK: improve observer confidence" in out
    assert "## 过程错题（执行/思考）" in out
    assert "execution_error / pr_merge" in out


def test_awareness_empty_inputs_still_generates(tmp_path: Path):
    run_id = "run-2026-02-24-observer-awareness-digest-empty"
    (tmp_path / "reports").mkdir(parents=True)
    (tmp_path / "TASKS").mkdir(parents=True)
    (tmp_path / "TASKS" / "QUEUE.md").write_text("# QUEUE\n\n## Queue\n", encoding="utf-8")

    res = _run_observe(tmp_path, run_id)
    assert res.returncode == 0, res.stdout + res.stderr

    out_file = tmp_path / "reports" / run_id / "awareness.md"
    assert out_file.exists()
    out = out_file.read_text(encoding="utf-8")
    assert "## 本周 shipped runs" in out
    assert "## 重复失败模式" in out
    assert "## 过程错题（执行/思考）" in out
    assert "## 当前风险" in out
    assert "## 下一枪建议" in out
