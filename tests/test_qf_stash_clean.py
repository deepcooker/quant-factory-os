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
    (repo / "TASKS").mkdir(parents=True)
    shutil.copy2(repo_root / "tools" / "qf", repo / "tools" / "qf")
    mode = os.stat(repo / "tools" / "qf").st_mode
    os.chmod(repo / "tools" / "qf", mode | stat.S_IXUSR)

    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test User"], cwd=repo)
    (repo / "tracked.txt").write_text("seed\n", encoding="utf-8")
    run(["git", "add", "."], cwd=repo)
    run(["git", "commit", "-m", "seed"], cwd=repo)
    return repo


def create_stash(repo: Path, message: str, marker: str) -> None:
    tracked = repo / "tracked.txt"
    tracked.write_text(tracked.read_text(encoding="utf-8") + marker + "\n", encoding="utf-8")
    res = run(["git", "stash", "push", "-m", message], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr


def test_qf_stash_clean_preview_and_apply(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)

    create_stash(repo, "ship-wip-1", "a")
    create_stash(repo, "manual-note-keep", "b")
    create_stash(repo, "qf-init-wip-2", "c")
    create_stash(repo, "resume-cleanup-run-3", "d")

    preview = run(["bash", "tools/qf", "stash-clean", "preview", "KEEP=1"], cwd=repo)
    assert preview.returncode == 0, preview.stdout + preview.stderr
    assert "stash-clean mode=preview" in preview.stdout
    assert "next: tools/qf stash-clean apply KEEP=1" in preview.stdout

    apply = run(["bash", "tools/qf", "stash-clean", "apply", "KEEP=0"], cwd=repo)
    assert apply.returncode == 0, apply.stdout + apply.stderr
    assert "stash-clean done: dropped=" in apply.stdout

    stash_list = run(["git", "stash", "list"], cwd=repo)
    assert stash_list.returncode == 0, stash_list.stdout + stash_list.stderr
    out = stash_list.stdout
    assert "ship-wip-" not in out
    assert "qf-init-wip-" not in out
    assert "resume-cleanup-run-" not in out
    assert "manual-note-keep" in out


def test_qf_stash_clean_no_candidates(tmp_path: Path) -> None:
    repo = setup_repo(tmp_path)
    create_stash(repo, "manual-note-only", "x")

    res = run(["bash", "tools/qf", "stash-clean"], cwd=repo)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "no qf/ship cleanup stashes found" in res.stdout
