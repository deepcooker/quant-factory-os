import os
import subprocess
from pathlib import Path


def run_view(path: str, allow_override: bool = False) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    if allow_override:
        env["CODEX_READ_DENYLIST_ALLOW"] = "1"
    return subprocess.run(
        ["bash", "tools/view.sh", path, "--from", "1", "--to", "1"],
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def test_view_blocks_denylisted_file_by_default():
    res = run_view("project_all_files.txt")
    assert res.returncode != 0
    combined = res.stdout + res.stderr
    assert ".codex_read_denylist" in combined
    assert "project_all_files.txt" in combined


def test_view_allows_denylisted_file_with_override():
    denylisted = Path("project_all_files.txt")
    denylisted.write_text("sample\n", encoding="utf-8")
    try:
        res = run_view("project_all_files.txt", allow_override=True)
        assert res.returncode == 0
        assert res.stdout.strip() != ""
        combined = res.stdout + res.stderr
        assert "override enabled" in combined
    finally:
        denylisted.unlink(missing_ok=True)
