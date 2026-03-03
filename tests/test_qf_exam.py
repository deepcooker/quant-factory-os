import os
import json
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
    (repo / "SYNC").mkdir(parents=True)

    shutil.copy2(repo_root / "tools" / "qf", repo / "tools" / "qf")
    shutil.copy2(repo_root / "tools" / "sync_exam.py", repo / "tools" / "sync_exam.py")
    shutil.copy2(repo_root / "SYNC" / "EXAM_RUBRIC.json", repo / "SYNC" / "EXAM_RUBRIC.json")
    mode = os.stat(repo / "tools" / "qf").st_mode
    os.chmod(repo / "tools" / "qf", mode | stat.S_IXUSR)

    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test User"], cwd=repo)
    return repo


def write_state(repo: Path, run_id: str) -> None:
    (repo / "TASKS" / "STATE.md").write_text(
        "\n".join(
            [
                "# STATE",
                f"CURRENT_RUN_ID: {run_id}",
                "CURRENT_TASK_FILE: TASKS/TASK-x.md",
                "CURRENT_STATUS: active",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def write_min_pass_answer(path: Path, rubric_file: Path) -> None:
    rubric = json.loads(rubric_file.read_text(encoding="utf-8"))
    checks = rubric.get("checks", [])
    seen: set[str] = set()
    lines: list[str] = []
    body = (
        "本段回答覆盖项目背景、阶段、workflow、entites、生命周期、branch/PR、review、summary、decision、"
        "自动化与优化，并给出证据路径：AGENTS.md、docs/WORKFLOW.md、docs/PROJECT_GUIDE.md、docs/ENTITIES.md、"
        "TASKS/STATE.md、TASKS/QUEUE.md、reports/run-current/summary.md、reports/run-current/decision.md；"
        "同时包含关键词：CURRENT_RUN_ID、插件、独立、codex、learn、ready、init、do、产品、架构、研发、测试、"
        "方向、保存、多角色、生命周期、偏离、下一步命令、orient、choose、council、arbiter、推理、"
        "conversation.md、decision.md、自动化、优先级、优化。"
    )
    for item in checks:
        section = str(item.get("section", "")).strip()
        if not section or section in seen:
            continue
        seen.add(section)
        lines.extend([f"## {section}", body, ""])

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def test_qf_exam_defaults_to_current_run_id(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    write_state(repo, "run-current")
    answer = repo / "reports" / "run-current" / "onboard_answer.md"
    write_min_pass_answer(answer, repo / "SYNC" / "EXAM_RUBRIC.json")

    res = run(["bash", "tools/qf", "exam"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "SYNC_EXAM_PASS: true" in res.stdout
    assert (repo / "reports" / "run-current" / "sync_exam_result.json").exists()


def test_qf_exam_supports_custom_paths(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    write_state(repo, "run-current")
    answer = repo / "reports" / "run-current" / "answer-custom.md"
    write_min_pass_answer(answer, repo / "SYNC" / "EXAM_RUBRIC.json")

    res = run(
        [
            "bash",
            "tools/qf",
            "exam",
            "RUN_ID=run-current",
            f"ANSWER_FILE={answer}",
            "OUTPUT_FILE=reports/run-current/result-custom.json",
        ],
        cwd=repo,
    )
    assert res.returncode == 0, res.stdout + res.stderr
    assert (repo / "reports" / "run-current" / "result-custom.json").exists()


def test_qf_exam_fails_when_answer_missing(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    write_state(repo, "run-current")
    res = run(["bash", "tools/qf", "exam"], cwd=repo)
    assert res.returncode != 0
    assert "answer file not found" in (res.stdout + res.stderr).lower()
