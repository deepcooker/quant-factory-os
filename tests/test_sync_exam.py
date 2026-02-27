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


def test_sync_exam_pass(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parents[1]
    answer = tmp_path / "answer.md"
    output = tmp_path / "result.json"
    answer.write_text(
        "\n".join(
            [
                "## 终点一致",
                "自动化、自我迭代、涌现智能是当前一致终点，本轮动作服务长期闭环，且本次同频要确保后续执行与终点因果一致。",
                "",
                "## 阶段一致",
                "当前阶段是同频治理强化，下一阶段进入稳定自动化切换，切换条件是门禁通过并且证据链可审计。",
                "",
                "## 上轮停止原因与恢复状态",
                "上轮是 tool_or_script_error，当前已恢复并在 main 继续。",
                "",
                "## 边界与非目标",
                "边界是证据链和门禁不破坏，non-goals 是不改业务策略。",
                "",
                "## 近况与最近提交",
                "最近 PR 与 RUN_ID 已更新，项目近况是治理层稳定推进。",
                "",
                "## 下一步单命令",
                "命令：tools/qf ready",
                "",
                "## 失败回退命令",
                "命令：tools/qf resume RUN_ID=run-2026-02-27-sync-learning-exam-cli-web",
                "",
                "## 学习更新清单",
                "复习宪法、工作流、证据规则。",
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
    assert any(x["id"] == "north_star" for x in payload["failed_checks"])
