from pathlib import Path


def test_ship_has_retry_and_resume_state_markers():
    repo_root = Path(__file__).resolve().parents[1]
    content = (repo_root / "tools" / "ship.sh").read_text(encoding="utf-8")

    assert "ship_state.json" in content
    assert "mistake_log.jsonl" in content
    assert "append_mistake_event" in content
    assert "run_with_retry_capture \"push\" git push -u origin \"$branch\"" in content
    assert "run_with_retry_capture \"pr_create\" gh pr create" in content
    assert "run_with_retry_capture \"pr_merge\" gh pr merge --squash --delete-branch \"$pr_url\"" in content
    assert "tools/qf resume RUN_ID=" in content
