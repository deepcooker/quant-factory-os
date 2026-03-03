import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def write_min_pass_answer(path: Path, rubric_file: Path) -> None:
    rubric = json.loads(rubric_file.read_text(encoding="utf-8"))
    checks = rubric.get("checks", [])
    seen: set[str] = set()
    lines: list[str] = []
    body = (
        "本段覆盖项目目标、阶段、workflow、entities、task/pr/run/project、方向讨论、branch/PR 管理、"
        "review/summary/decision，以及 codex 实操与主线判断；证据路径包括 AGENTS.md、docs/WORKFLOW.md、"
        "docs/PROJECT_GUIDE.md、docs/ENTITIES.md、TASKS/STATE.md、TASKS/QUEUE.md、reports/run-x/summary.md；"
        "并明确写出关键词：独立、插件、推理、conversation.md、decision.md、偏离、orient、choose、council、arbiter、"
        "产品、架构、研发、测试、自动化、优先级、优化、下一步、命令。"
    )
    for item in checks:
        section = str(item.get("section", "")).strip()
        if not section or section in seen:
            continue
        seen.add(section)
        lines.extend([f"## {section}", body, ""])
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def test_sync_exam_pass(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    answer = tmp_path / "answer.md"
    output = tmp_path / "result.json"
    write_min_pass_answer(answer, repo / "SYNC" / "EXAM_RUBRIC.json")

    res = run(
        [
            sys.executable,
            "tools/sync_exam.py",
            "--answer-file",
            str(answer),
            "--output-file",
            str(output),
            "--run-id",
            "run-2026-02-27-sync-learning-exam-cli-web",
        ],
        cwd=repo,
    )
    assert res.returncode == 0, res.stdout + res.stderr
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["passed"] is True
    assert payload["score"] >= payload["pass_score"]


def test_sync_exam_fail_on_missing_required(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    answer = tmp_path / "answer_fail.md"
    output = tmp_path / "result_fail.json"
    answer.write_text(
        "\n".join(
            [
                "## 阶段一致",
                "当前阶段已定义。",
                "",
                "## 下一步单命令",
                "命令：tools/qf ready",
                "",
                "## 失败回退命令",
                "命令：tools/qf resume RUN_ID=run-x",
                "",
            ]
        ),
        encoding="utf-8",
    )

    res = run(
        [
            sys.executable,
            "tools/sync_exam.py",
            "--answer-file",
            str(answer),
            "--output-file",
            str(output),
            "--run-id",
            "run-x",
        ],
        cwd=repo,
    )
    assert res.returncode == 1, res.stdout + res.stderr
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["passed"] is False
    assert any(x["id"] == "q1_mission" for x in payload["failed_checks"])
