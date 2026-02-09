import os
import subprocess


def test_ship_pr_body_excerpt_writes_file_and_stdout(tmp_path):
    run_id = "run-test-ship-pr-body-excerpt"
    pr_body = "\n".join(
        [
            "## 任务文件",
            "",
            "- 路径：`TASKS/TASK-ship-echo-prbody.md`",
            "- 标题：TASK: ship echo PR body excerpts",
            "",
            "## Evidence paths",
            "```",
            "reports/run-test-ship-pr-body-excerpt/meta.json",
            "reports/run-test-ship-pr-body-excerpt/summary.md",
            "reports/run-test-ship-pr-body-excerpt/decision.md",
            "```",
            "",
            "## 变更概述",
            "- other content",
        ]
    )
    expected_excerpt = "\n".join(
        [
            "## 任务文件",
            "",
            "- 路径：`TASKS/TASK-ship-echo-prbody.md`",
            "- 标题：TASK: ship echo PR body excerpts",
            "",
            "## Evidence paths",
            "```",
            "reports/run-test-ship-pr-body-excerpt/meta.json",
            "reports/run-test-ship-pr-body-excerpt/summary.md",
            "reports/run-test-ship-pr-body-excerpt/decision.md",
            "```",
        ]
    )

    env = os.environ.copy()
    env["SHIP_PR_BODY_EXCERPT_ONLY"] = "1"
    env["SHIP_PR_BODY_EXCERPT_RUN_ID"] = run_id
    env["SHIP_PR_BODY_EXCERPT_INPUT"] = pr_body
    env["RUN_ID"] = run_id

    res = subprocess.run(
        ["bash", "tools/ship.sh", "test: pr body excerpt"],
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )

    assert res.returncode == 0, res.stderr
    assert expected_excerpt in res.stdout

    excerpt_path = os.path.join("reports", run_id, "pr_body_excerpt.md")
    with open(excerpt_path, "r", encoding="utf-8") as handle:
        content = handle.read().strip()
    assert content == expected_excerpt

    os.remove(excerpt_path)
    try:
        os.rmdir(os.path.join("reports", run_id))
    except OSError:
        pass
