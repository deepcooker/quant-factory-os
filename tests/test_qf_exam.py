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


def write_min_pass_answer(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "## 终点一致",
                "自动化、自我迭代、涌现智能是一致终点，这次动作用于保证学习同频并支撑后续执行闭环。",
                "",
                "## 阶段一致",
                "当前阶段是同频治理，下一阶段是稳定自动化推进，切换以门禁和证据为条件。",
                "",
                "## 上轮停止原因与恢复状态",
                "上轮属于 tool_or_script_error，当前已恢复到 main 并可继续推进。",
                "",
                "## 边界与非目标",
                "边界是流程门禁和证据链，non-goals 是不改业务策略和交易逻辑。",
                "",
                "## 近况与最近提交",
                "最近 PR 与 RUN_ID 已更新，当前近况是同频考试机制落地。",
                "",
                "## 下一步单命令",
                "命令：tools/qf handoff",
                "",
                "## 失败回退命令",
                "命令：tools/qf resume RUN_ID=run-current",
                "",
                "## 学习更新清单",
                "复习考试题面、模板与评分规则。",
                "",
            ]
        ),
        encoding="utf-8",
    )


def test_qf_exam_defaults_to_current_run_id(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    write_state(repo, "run-current")
    answer = repo / "reports" / "run-current" / "onboard_answer.md"
    write_min_pass_answer(answer)

    res = run(["bash", "tools/qf", "exam"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "SYNC_EXAM_PASS: true" in res.stdout
    assert (repo / "reports" / "run-current" / "sync_exam_result.json").exists()


def test_qf_exam_supports_custom_paths(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    write_state(repo, "run-current")
    answer = repo / "reports" / "run-current" / "answer-custom.md"
    write_min_pass_answer(answer)

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
