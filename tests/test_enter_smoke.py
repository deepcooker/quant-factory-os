import os
import subprocess
import tempfile


def run_enter(cwd: str):
    repo_root = os.path.abspath(os.getcwd())
    return subprocess.run(
        ["bash", os.path.join(repo_root, "tools", "enter.sh")],
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
    )


def test_enter_fails_outside_repo_root():
    with tempfile.TemporaryDirectory() as tmpdir:
        res = run_enter(tmpdir)
    assert res.returncode != 0
    assert "仓库根目录" in (res.stdout + res.stderr)


def test_enter_fails_on_dirty_repo():
    repo_root = os.path.abspath(os.getcwd())
    temp_path = os.path.join(repo_root, "reports", "run-2026-02-09-enter", "enter_dirty.tmp")
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)
    with open(temp_path, "w", encoding="utf-8") as handle:
        handle.write("dirty\n")
    try:
        res = run_enter(repo_root)
        assert res.returncode != 0
        assert "工作区不干净" in (res.stdout + res.stderr)
    finally:
        os.remove(temp_path)
