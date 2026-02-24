from pathlib import Path


def test_ship_waits_for_merge_before_sync_and_emits_sync_marker():
    repo_root = Path(__file__).resolve().parents[1]
    content = (repo_root / "tools" / "ship.sh").read_text(encoding="utf-8")

    assert "wait_for_pr_merged()" in content
    assert "gh pr view \"$pr_url\" --json state -q .state" in content
    assert "waiting merge... (state=" in content
    assert "wait_for_pr_merged \"$pr_url\"" in content

    wait_idx = content.index("wait_for_pr_merged \"$pr_url\"")
    checkout_idx = content.rindex("git checkout main")
    pull_idx = content.rindex("git pull --rebase origin main")
    assert wait_idx < checkout_idx < pull_idx

    assert "post-ship synced main@" in content
