from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_task_ship_script_exists() -> None:
    ship = REPO_ROOT / "tools" / "ship.sh"
    assert ship.exists(), "tools/ship.sh is missing"


def test_task_ship_usage_without_message() -> None:
    result = subprocess.run(
        ["bash", "tools/ship.sh"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "用法：tools/ship.sh" in (result.stderr + result.stdout)


def test_task_ship_defaults_to_current_base_branch() -> None:
    text = (REPO_ROOT / "tools" / "ship.sh").read_text(encoding="utf-8")
    assert 'base_branch="${SHIP_BASE_BRANCH:-$orig_branch}"' in text
    assert 'pr_base_branch="${SHIP_PR_BASE_BRANCH:-$base_branch}"' in text
    assert 'git checkout -b "$branch" "$base_branch"' in text
    assert 'gh pr create --base "$pr_base_branch"' in text
    assert 'git checkout "$base_branch"' in text


def test_task_ship_ignores_own_ship_state_in_post_sync_dirty_check() -> None:
    text = (REPO_ROOT / "tools" / "ship.sh").read_text(encoding="utf-8")
    assert 'ship_state_rel="reports/${run_id}/ship_state.json"' in text
    assert 'if [[ "$line" == "$ship_state_rel" ]]; then' in text
    assert "if has_blocking_dirty_paths; then" in text


def test_task_ship_checks_merge_state_before_pr_merge() -> None:
    text = (REPO_ROOT / "tools" / "ship.sh").read_text(encoding="utf-8")
    assert 'gh pr view "$pr_url" --json mergeStateStatus -q .mergeStateStatus' in text
    assert 'if [[ "$merge_state" != "CLEAN" && "$merge_state" != "UNKNOWN" ]]; then' in text
    assert 'fail_pr_merge_blocked "$merge_state"' in text
