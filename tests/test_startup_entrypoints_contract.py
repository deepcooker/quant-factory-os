from pathlib import Path


def test_enter_lists_startup_entrypoints_and_run_id():
    repo_root = Path(__file__).resolve().parents[1]
    enter_text = (repo_root / "tools" / "enter.sh").read_text(encoding="utf-8")

    assert "Entry points:" in enter_text
    assert "- TASKS/STATE.md" in enter_text
    assert "- TASKS/QUEUE.md" in enter_text
    assert "- docs/WORKFLOW.md#Codex-session-startup-checklist" in enter_text
    assert 'RUN_ID: ${RUN_ID:-"(not set)"}' in enter_text


def test_start_delegates_to_enter():
    repo_root = Path(__file__).resolve().parents[1]
    start_text = (repo_root / "tools" / "start.sh").read_text(encoding="utf-8")

    assert "bash tools/enter.sh" in start_text
