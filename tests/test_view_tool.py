import os
import subprocess


def run_view(args):
    return subprocess.run(
        ["bash", "tools/view.sh", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_view_tool_reads_range_inside_repo():
    run_id = "run-2026-02-09-view-tool"
    base_dir = os.path.join("reports", run_id)
    os.makedirs(base_dir, exist_ok=True)
    path = os.path.join(base_dir, "view_tool_fixture.txt")
    with open(path, "w", encoding="utf-8") as handle:
        for idx in range(1, 11):
            handle.write(f"line{idx}\n")

    res = run_view([path, "--from", "2", "--to", "4"])
    assert res.returncode == 0
    assert res.stdout == "line2\nline3\nline4\n"

    os.remove(path)


def test_view_tool_rejects_excessive_range():
    run_id = "run-2026-02-09-view-tool"
    base_dir = os.path.join("reports", run_id)
    os.makedirs(base_dir, exist_ok=True)
    path = os.path.join(base_dir, "view_tool_fixture.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("line1\n")

    res = run_view([path, "--from", "1", "--to", "300"])
    assert res.returncode != 0
    assert "请分段查看" in (res.stdout + res.stderr)

    os.remove(path)


def test_view_tool_rejects_outside_repo():
    res = run_view(["/etc/hosts"])
    assert res.returncode != 0
