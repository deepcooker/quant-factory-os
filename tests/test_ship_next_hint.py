from pathlib import Path


def test_ship_script_contains_next_shot_hint_block():
    repo_root = Path(__file__).resolve().parents[1]
    content = (repo_root / "tools" / "ship.sh").read_text(encoding="utf-8")
    assert "== 下一枪建议 ==" in content
    assert "如果 QUEUE 还有 [ ]：运行 tools/task.sh --next" in content
