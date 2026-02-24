import os
import subprocess
from pathlib import Path


def test_ship_queue_mark_done_only_updates_queue(tmp_path: Path):
    queue = tmp_path / "QUEUE.md"
    rid = "run-2026-02-22-auto-mark"
    queue.write_text(
        "\n".join(
            [
                "# QUEUE",
                "",
                "## Queue",
                f"- [>] TODO Title: x  Picked: {rid} 2026-02-22T00:00:00+0800",
            ]
        ),
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["SHIP_QUEUE_MARK_DONE_ONLY"] = "1"
    env["SHIP_QUEUE_MARK_DONE_QUEUE_FILE"] = str(queue)
    env["SHIP_QUEUE_MARK_DONE_RUN_ID"] = rid
    env["SHIP_QUEUE_MARK_DONE_PR_URL"] = "https://github.com/deepcooker/quant-factory-os/pull/123"

    res = subprocess.run(
        ["bash", "tools/ship.sh", "test: queue mark done"],
        env=env,
        text=True,
        capture_output=True,
    )
    assert res.returncode == 0, res.stdout + res.stderr

    updated = queue.read_text(encoding="utf-8")
    assert "- [x]" in updated
    assert "Picked:" in updated
    assert "Done: PR #123" in updated
    assert f"RUN_ID={rid}" in updated
